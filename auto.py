import json
import time
import serial 
from detections import HailoDetectionRunner
from drive_movement import drive_backward, drive_forward, turn_left, turn_right, stop_robot
#from ai_camera import IMX500Detector

ser = serial.Serial("/dev/ttyAMA0", 9600)


def move_toward_person(x_center):
    
    if x_center >= 0.9 or x_center <= 0.9:
        drive_backward("LOW")
        time.sleep(0.3) 
        stop_robot()
    elif x_center >= 0.67:
        turn_right("LOW")
    elif x_center <= 0.33:
        turn_left("LOW")
    elif 0.34 < x_center < 0.66:
        drive_forward("LOW")
    elif output_data == []:
        stop_robot()


def act_on_detections(detections, labels):
    for d in detections:
        label = d["label"]
        confidence = d["confidence"]
        if label == "person" and confidence > 0.6:
            x = d["bbox"]["x"]
            w = d["bbox"]["w"]
            x_center = (x + w / 2) / 640
            move_toward_person(x_center)
            return
        else:
            stop_robot()
            return
            

print("Running Hailo object detection with autonomous movement")

detection_runner = HailoDetectionRunner()
detection_runner.start()

try:
    while True:
        detections = detection_runner.get_latest_detections()
        labels = ["person"]
        output_data = detections

        with open("detections.json", "w") as f:
            json.dump(output_data, f, indent=2)

        act_on_detections(detections, labels)

        if output_data == []:
            ser.write(bytes([64, 192]))

        time.sleep(0.5)

except KeyboardInterrupt:
    print("Shutting down..")
    stop_robot()
    ser.close()
    detection_runner.stop()



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


    # except KeyboardInterrupt:
    #     print("Shutting down..")
    #     stop_robot()
    #     ser.close()
    #     camera.stop()
