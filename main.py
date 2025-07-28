from drive import Controller
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import hailo
from hailo_apps.hailo_app_python.core.gstreamer.gstreamer_app import app_callback_class
from hailo_apps.hailo_app_python.apps.detection_simple.detection_pipeline_simple import GStreamerDetectionApp
import threading
import time


c = Controller()


def mow_lawn():
    time.sleep(5)
    print("finsihed mowing the lawn")




def walk_jordan():
    
    time.sleep(2)
    print("finsihed walking jordan")



task1 = threading.Thread(target=mow_lawn)
task1.start()
task2 = threading.Thread(target=walk_jordan)
task2.start()
