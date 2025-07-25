from pathlib import Path
import gi
gi.require_version('Gst', '1.0')
import time
from gi.repository import Gst, GLib
import os
import numpy as np
import cv2
import hailo
import json
from hailo_apps.hailo_app_python.core.common.buffer_utils import get_caps_from_pad, get_numpy_from_buffer
from hailo_apps.hailo_app_python.core.gstreamer.gstreamer_app import app_callback_class
from hailo_apps.hailo_app_python.apps.detection.detection_pipeline import GStreamerDetectionApp
from drive_movement import drive_backward, drive_forward, turn_left, turn_right, stop_robot
#import keyboard

# -----------------------------------------------------------------------------------------------
# User-defined class to be used in the callback function
# -----------------------------------------------------------------------------------------------
# Inheritance from the app_callback_class
class user_app_callback_class(app_callback_class):
    def __init__(self):
        super().__init__()
        self.new_variable = 42  # New variable example

    def new_function(self):  # New function example
        return "The meaning of life is: "

# -----------------------------------------------------------------------------------------------
# User-defined callback function
# -----------------------------------------------------------------------------------------------

# This is the callback function that will be called when data is available from the pipeline
def app_callback(pad, info, user_data):
    # Get the GstBuffer from the probe info
    buffer = info.get_buffer()
    # Check if the buffer is valid
    if buffer is None:
        return Gst.PadProbeReturn.OK

    # Using the user_data to count the number of frames
    user_data.increment()
    string_to_print = f"Frame count: {user_data.get_count()}\n"

    # Get the caps from the pad
    format, width, height = get_caps_from_pad(pad)

    # If the user_data.use_frame is set to True, we can get the video frame from the buffer
    frame = None
    if user_data.use_frame and format is not None and width is not None and height is not None:
        # Get video frame
        frame = get_numpy_from_buffer(buffer, format, width, height)

    # Get the detections from the buffer
    roi = hailo.get_roi_from_buffer(buffer)
    detections = roi.get_objects_typed(hailo.HAILO_DETECTION)
    landmarks = roi.get_objects_typed(hailo.HAILO_LANDMARKS)
    
    # for landmark in landmarks: 
    #     coords = landmark.get_points()
    #     landmark_type = landmark.get_type()
    #     # W_string += (f"Landmark Type: {landmark_type}")

    # Parse the detections
    detection_count = 0
    for detection in detections:
        label = detection.get_label()
        bbox = detection.get_bbox()
        confidence = detection.get_confidence()
        
        # print()
        # print(dir(bbox))
        #print(type(bbox))
        if label == "person":
            output_data = []
            x_min = bbox.xmin()
            y_min = bbox.ymin()
            x_max = bbox.xmax()
            y_max = bbox.ymax()
            x_center = x_max - x_min
            y_center = y_max - y_min

            output_data.append({
                "label": label,
                "confidence": confidence,
                "x center": x_center,
                "y center": y_center,
            })
            with open("detections_hailo.json", "w") as f:
                jsona.dump(output_data, f, indent=2)

            def move_toward_person(x_center):
                if x_center >= 0.9 or x_center <= 0.1:
                    drive_backward("LOW")
                    time.sleep(0.3)
                    stop_robot()
                elif x_center >= 0.67:
                    turn_right("LOW")
                elif x_center <= 0.33:
                    turn_left("LOW")
                elif 0.34 < x_center < 0.66:
                    drive_forward("LOW")

            def act_on_detections(detection):
                if not detection:
                    stop_robot()
                    return
                else:
                    move_toward_person(x_center)
                    return
            stop_robot()

            #time.sleep(.25)


            # Get track ID
            track_id = 0
            track = detection.get_objects_typed(hailo.HAILO_UNIQUE_ID)
            if len(track) == 1:
                track_id = track[0].get_id()
            #string_to_print += (f"Detection: ID: {track_id} Label: {label} Confidence: {confidence:.2f}\n, Center Point: {x_center, y_center}")
            detection_count += 1
    if user_data.use_frame:
        # Note: using imshow will not work here, as the callback function is not running in the main thread
        # Let's print the detection count to the frame
        cv2.putText(frame, f"Detections: {detection_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Example of how to use the new_variable and new_function from the user_data
        # Let's print the new_variable and the result of the new_function to the frame
        cv2.putText(frame, f"{user_data.new_function()} {user_data.new_variable}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Convert the frame to BGR
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        user_data.set_frame(frame)

    act_on_detections(detections)
    # if keyboard.is_pressed(keyboard.KEY_DOWN):
    #     print("Shutting Down...")
    #     stop_robot()

    #print(string_to_print)
    return Gst.PadProbeReturn.OK

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    env_file     = project_root / ".env"
    env_path_str = str(env_file)
    os.environ["HAILO_ENV_FILE"] = env_path_str
    # Create an instance of the user app callback class
    user_data = user_app_callback_class()
    app = GStreamerDetectionApp(app_callback, user_data)
    app.run()





















# from pathlib import Path
# import gi
# gi.require_version('Gst', '1.0')
# from gi.repository import Gst, GLib
# import os
# import numpy as np
# import cv2
# import hailo

# from hailo_apps.hailo_app_python.core.common.buffer_utils import get_caps_from_pad, get_numpy_from_buffer
# from hailo_apps.hailo_app_python.core.gstreamer.gstreamer_app import app_callback_class
# from hailo_apps.hailo_app_python.apps.detection.detection_pipeline import GStreamerDetectionApp

# # -----------------------------------------------------------------------------------------------
# # User-defined class to be used in the callback function
# # -----------------------------------------------------------------------------------------------
# # Inheritance from the app_callback_class
# class user_app_callback_class(app_callback_class):
#     def __init__(self):
#         super().__init__()
#         self.new_variable = 42  # New variable example

#     def new_function(self):  # New function example
#         return "The meaning of life is: "

# # -----------------------------------------------------------------------------------------------
# # User-defined callback function
# # -----------------------------------------------------------------------------------------------

# # This is the callback function that will be called when data is available from the pipeline
# def app_callback(pad, info, user_data):
#     # Get the GstBuffer from the probe info
#     buffer = info.get_buffer()
#     # Check if the buffer is valid
#     if buffer is None:
#         return Gst.PadProbeReturn.OK

#     # Using the user_data to count the number of frames
#     user_data.increment()
#     string_to_print = f"Frame count: {user_data.get_count()}\n"

#     # Get the caps from the pad
#     format, width, height = get_caps_from_pad(pad)

#     # If the user_data.use_frame is set to True, we can get the video frame from the buffer
#     frame = None
#     if user_data.use_frame and format is not None and width is not None and height is not None:
#         # Get video frame
#         frame = get_numpy_from_buffer(buffer, format, width, height)

#     # Get the detections from the buffer
#     roi = hailo.get_roi_from_buffer(buffer)
#     detections = roi.get_objects_typed(hailo.HAILO_DETECTION)

#     # Parse the detections
#     detection_count = 0
#     for detection in detections:
#         label = detection.get_label()
#         bbox = detection.get_bbox()
#         confidence = detection.get_confidence()
#         if label == "person":
#             # Get track ID
#             track_id = 0
#             track = detection.get_objects_typed(hailo.HAILO_UNIQUE_ID)
#             if len(track) == 1:
#                 track_id = track[0].get_id()
#             string_to_print += (f"Detection: ID: {track_id} Label: {label} Confidence: {confidence:.2f}\n")
#             detection_count += 1
#     if user_data.use_frame:
#         # Note: using imshow will not work here, as the callback function is not running in the main thread
#         # Let's print the detection count to the frame
#         cv2.putText(frame, f"Detections: {detection_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
#         # Example of how to use the new_variable and new_function from the user_data
#         # Let's print the new_variable and the result of the new_function to the frame
#         cv2.putText(frame, f"{user_data.new_function()} {user_data.new_variable}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
#         # Convert the frame to BGR
#         frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
#         user_data.set_frame(frame)

#     print(string_to_print)
#     return Gst.PadProbeReturn.OK

# if __name__ == "__main__":
#     project_root = Path(__file__).resolve().parent.parent
#     env_file     = project_root / ".env"
#     env_path_str = str(env_file)
#     os.environ["HAILO_ENV_FILE"] = env_path_str
#     # Create an instance of the user app callback class
#     user_data = user_app_callback_class()
#     app = GStreamerDetectionApp(app_callback, user_data)
#     app.run()
    
# # Added part to get Hailo detections for robot control
# class HailoDetectionRunner:
#     def __init__(self):
#         from threading import Thread
#         self.detections = []
#         self.user_data = user_app_callback_class()
#         self.user_data.set_frame(None)
#         self.app = GStreamerDetectionApp(self._callback, self.user_data)
#         self.thread = Thread(target=self.app.run)
#         self.running = False

#     def _callback(self, pad, info, user_data):
#         buffer = info.get_buffer()
#         if buffer is None:
#             return Gst.PadProbeReturn.OK

#         roi = hailo.get_roi_from_buffer(buffer)
#         detections = roi.get_objects_typed(hailo.HAILO_DETECTION)

#         results = []
#         for detection in detections:
#             label = detection.get_label()
#             bbox = detection.get_bbox()
#             confidence = detection.get_confidence()
#             if label == "person":
#                 try:
#                     x = bbox.x
#                     y = bbox.y 
#                     h = bbox.height
#                     w = bbox.width
#                 except AttributeError as e:
#                     print("Fallback")
#                 return GStreamerDetectionApp
#                 results.append({
#                     "label": label,
#                     "confidence": confidence,
#                     "bbox": {"x": x, "y": y, "w": w, "h": h}
#                 })

#         self.detections = results
#         return Gst.PadProbeReturn.OK

#     def start(self):
#         if not self.running:
#             self.running = True
#             self.thread.start()

#     def stop(self):
#         if self.running:
#             self.app.stop()
#             self.thread.join()
#             self.running = False

#     def get_latest_detections(self):
#         return self.detections
