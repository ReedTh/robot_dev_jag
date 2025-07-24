from pathlib import Path
import threading
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
import os
import cv2
import hailo
import time
import serial
from hailo_apps.hailo_app_python.core.common.buffer_utils import get_caps_from_pad, get_numpy_from_buffer
from hailo_apps.hailo_app_python.core.gstreamer.gstreamer_app import app_callback_class
from hailo_apps.hailo_app_python.apps.detection.detection_pipeline import GStreamerDetectionApp
from drive_movement import stop_robot


ser =  serial.Serial("/dev/ttyAMA0", 9600)



class Publisher:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, subscriber, topic):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(subscriber)

    def publish(self, message, topic):
        if topic in self.subscribers:
            for subscriber in self.subscribers[topic]:
                subscriber.event.set()
                subscriber.message = message


class Subscriber:
        
    def __init__(self, name):
        self.name = name
        self.event = threading.Event()
        self.message = None

    def receive(self):
        self.event.wait()
        move_toward_person_left()
        move_toward_person_right()
        self.event.clear()


# Defining left movement

def drive_forward_left(speed):

    if speed.upper() == "HIGH":
        ser.write(bytes([129]))
    elif speed.upper() == "MID":
        ser.write(bytes([160]))
    elif speed.upper() == "LOW": 
        ser.write(bytes([191]))
    else:
        ser.write(bytes([0]))
        
def drive_backward_left(speed):

    if speed.upper() == "HIGH":
        ser.write(bytes([254]))
    elif speed.upper() == "MID":
        ser.write(bytes([224]))
    elif speed.upper() == "LOW":
        ser.write(bytes([193]))

# Defining right movement

def drive_forward_right(speed):
    if speed.upper() == "HIGH":
        ser.write(bytes([127]))
    elif speed.upper() == "MID":
        ser.write(bytes([96]))
    elif speed.upper() == "LOW":
        ser.write(bytes([65]))

def drive_backward_right(speed):
    if speed.upper() == "HIGH":
        ser.write(bytes([1]))
    elif speed.upper() == "MID":
        ser.write(bytes([32]))
    elif speed.upper() == "LOW":
        ser.write(bytes([61]))

# Movement towards person 

def move_toward_person_left(x_center):

    if x_center >= 0.8 or x_center <= 0.2:
        drive_backward_left("MID")
        time.sleep(1)
        stop_robot()
    elif 0.21 <= x_center <=0.79:
        drive_forward_left("LOW")
    else:
        stop_robot()


def move_toward_person_right(x_center):
    if x_center >= 0.8 or x_center <= 0.2:
        drive_backward_right("LOW")
        time.sleep(0.3)
        stop_robot()
    # elif x_center >= 0.67:
    #     turn_right("LOW")
    # elif x_center <= 0.33:
    #     turn_left("LOW")
    elif 0.21 <= x_center <= 0.79:
        drive_forward_right("LOW")
    else:
        stop_robot()

class user_app_callback_class(app_callback_class):
    def __init__(self):
        super().__init__()



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


    detection_count = 0
    for detection in detections:
        label = detection.get_label()
        bbox = detection.get_bbox()
        confidence = detection.get_confidence()
        x_min = bbox.xmin()
        x_max = bbox.xmax()
        x_center = (x_max + x_min) / 2
        
        if label == "person":

            # Defining Pub/Sub relationship

            publisher = Publisher()

            subscriber_1 = Subscriber(move_toward_person_left())
            subscriber_2 = Subscriber(move_toward_person_right())
            
            publisher.subscribe(subscriber_1, "x_center_reading")
            publisher.subscribe(subscriber_2, "x_center_reading")

            publisher.publish(x_center, "x_center_reading")
                              
            subscriber_1.receive()
            subscriber_2.receive()
    

            # Get track ID
            track_id = 0
            track = detection.get_objects_typed(hailo.HAILO_UNIQUE_ID)
            if len(track) == 1:
                track_id = track[0].get_id()
            detection_count += 1

            def act_on_detections(detections, labels):
                if not detection:
                    stop_robot()
                    return
                else:
                    move_toward_person(x_center)
                    return
    if user_data.use_frame:
        # Note: using imshow will not work here, as the callback function is not running in the main thread
        # Let's print the detection count to the frame
        cv2.putText(frame, f"Detections: {detection_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Convert the frame to BGR
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        user_data.set_frame(frame)

    act_on_detections(x_center)

    print(string_to_print)
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

   
