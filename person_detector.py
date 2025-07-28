import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import hailo
from hailo_apps.hailo_app_python.core.gstreamer.gstreamer_app import app_callback_class
from hailo_apps.hailo_app_python.apps.detection_simple.detection_pipeline_simple import GStreamerDetectionApp



class user_app_callback_class(app_callback_class):
    def __init__(self):
        super().__init__()

class Person_center:
    def __init__(self):
        pass


    def app_callback(self, pad, info, user_data):
        user_data.increment()
        buffer = info.get_buffer()
        if buffer is None:
            return Gst.PadProbeReturn.OK
        detections = hailo.get_roi_from_buffer(buffer).get_objects_typed(hailo.HAILO_DETECTION)

        for det in detections:
                bbox = det.get_bbox()
                x_center = (bbox.xmin() + bbox.xmax()) / 2

            
if __name__ == "__main__":
    user_data = user_app_callback_class()
    app = GStreamerDetectionApp(Person_center.app_callback, user_data)
    app.run()
