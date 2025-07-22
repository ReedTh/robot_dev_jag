import json
import time
import serial
import os
from pathlib import Path

import cv2

from detections import app_callback, user_app_callback_class
from hailo_apps.hailo_app_python.apps.detection.detection_pipeline import GStreamerDetectionApp

from drive_movement import drive_backward, drive_forward, turn_left, turn_right, stop_robot

# Serial communication setup
ser = serial.Serial("/dev/ttyAMA0", 9600)

# Robot control logic
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

def act_on_detections(detections):
    if not detections:
        stop_robot()
        return

    for d in detections:
        if d["label"] == "person":
            x = d["bbox"]["x"]
            w = d["bbox"]["w"]
            x_center = (x + w / 2) / 640
            move_toward_person(x_center)
            return
    stop_robot()

# Main execution
if __name__ == "__main__":
    # Load Hailo environment
    project_root = Path(__file__).resolve().parent.parent
    env_file = project_root / ".env"
    os.environ["HAILO_ENV_FILE"] = str(env_file)

    # Set up detection app and user callback
    user_data = user_app_callback_class()
    user_data.use_frame = True  # Needed for preview window and frame access
    app = GStreamerDetectionApp(app_callback, user_data)

    print("Running Hailo detection with autonomous movement...")

    try:
        app.start()
        while True:
            detections = user_data.get_detections()

            # Save detections to JSON
            with open("detections.json", "w") as f:
                json.dump(detections, f, indent=2)

            # Robot movement logic
            act_on_detections(detections)

            # Fallback serial signal if no detection
            if not detections:
                ser.write(bytes([64, 192]))

            # Live video preview
            frame = user_data.get_frame()
            if frame is not None:
                cv2.imshow("Live Preview", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Shutting down...")

    finally:
        stop_robot()
        ser.close()
        app.stop()
        cv2.destroyAllWindows()













































# import json
# import time
# import serial 
# from drive_movement import drive_backward, drive_forward, turn_left, turn_right, stop_robot
# from ai_camera import IMX500Detector

# ser = serial.Serial("/dev/ttyAMA0", 9600)


# def move_toward_person(x_center):
    
#     if x_center >= 0.9 or x_center <= 0.9:
#         drive_backward("LOW")
#         time.sleep(0.3) 
#         stop_robot()
#     elif x_center >= 0.67:
#         turn_right("LOW")
#     elif x_center <= 0.33:
#         turn_left("LOW")
#     elif 0.34 < x_center < 0.66:
#         drive_forward("LOW")
#     elif output_data == []:
#         stop_robot()


# def act_on_detections(detections, labels):
#     for d in detections:
#         label = labels[int(d.category)]
#         confidence = float(d.conf)
#         if label == "person" and confidence > 0.6:
#             x, y, w, h = d.box
#             x_center = (x + w / 2) / 640
#             move_toward_person(x_center)
#             return
#         else:
#             stop_robot()
#             return
        
           

# if __name__ == "__main__":
#     camera = IMX500Detector()
#     camera.start(show_preview=True)

#     print("Running object deteciton with autonomous movement")

#     try:
#         while True:
#             detections = camera.get_detections()
#             labels = camera.get_labels()
            
#             output_data = []
#             for d in detections:
#                 label = labels[int(d.category)]
#                 confidence = float(d.conf)
#                 x, y, w, h = d.box
                
#                 output_data.append({
#                     "label": label,
#                     "confidence": confidence,
#                     "bbox": {"x": x, "y": y, "w": w, "h": h}
#                 })
                
#             with open("detections.json", "w") as f: 
#                 json.dump(output_data, f, indent=2)
                
#             act_on_detections(detections, labels)
            
#             if output_data == []:
#                 ser.write(bytes([64, 192]))
                
#             time.sleep(0.5)


#     except KeyboardInterrupt:
#         print("Shutting down..")
#         stop_robot()
#         ser.close()
#         camera.stop()

            
