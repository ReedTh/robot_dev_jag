import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import hailo
from hailo_apps.hailo_app_python.core.common.buffer_utils import get_caps_from_pad, get_numpy_from_buffer
from hailo_apps.hailo_app_python.core.gstreamer.gstreamer_app import app_callback_class
from hailo_apps.hailo_app_python.apps.detection_simple.detection_pipeline_simple import GStreamerDetectionApp
import os
from pathlib import Path
import numpy as np
import cv2
from drive_movement import drive_backward, drive_forward, stop_robot, turn_left, turn_right
import time


class user_app_callback_class(app_callback_class):
    def __init__(self):
        super().__init__()
        # self.total_people = 0
        # self.total_frames = 0
        # self.center = .5
        
# class Person_center:
#     def __init__(self):
#         self.pad = app_callback
#         self.info = -1
#         self.user_data = -1

def app_callback(pad, info, user_data):

    user_data.increment()
    buffer = info.get_buffer()
    if buffer is None:
        return Gst.PadProbeReturn.OK
    format, width, height = get_caps_from_pad(pad)
    frame = None
    if user_data.use_frame and format is not None and width is not None and height is not None:
        frame = get_numpy_from_buffer(buffer, format, width, height)
    
    roi = hailo.get_roi_from_buffer(buffer)
    detections = roi.get_objects_typed(hailo.HAILO_DETECTION)

    for det in detections:
        label = det.get_label()
        bbox = det.get_bbox()
        if label == "person":    
            x_center = (bbox.xmin() + bbox.xmax()) / 2


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

    print({x_center})
    act_on_detections(detections)
    return Gst.PadProbeReturn.OK

    


if __name__ == "__main__":
    # project_root = Path(__file__).resolve().parent.parent
    # env_file     = project_root / ".env"
    # env_path_str = str(env_file)
    # os.environ["HAILO_ENV_FILE"] = env_path_str
    # print(project_root)
    # print(env_file)
    # print(env_path_str)
    try: 
        while True:
            user_data = user_app_callback_class()
            # print(app_callback_class.frame_count)
            app = GStreamerDetectionApp(app_callback, user_data)
            app.run()
            
    except KeyboardInterrupt:
        print("Shutting down.....")
    finally:
        stop_robot()


    # c = Controller()
    # if user_data.center <= .33:
    #     c.drive_forward("LOW")
    # else:
    #     c.drive_backward("LOW")    
