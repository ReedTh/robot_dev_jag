import json
import time
import serial 
from ai_camera import IMX500Detector
#from controller_drive import main_controller
from drive_movement import drive_backward, drive_forward, turn_left, turn_right, stop_robot

ser = serial.Serial("/dev/ttyAMA0", 9600)


def move_toward_person(x_center):
 
    
    if x_center >= 0.67:
        turn_right("LOW")
    elif x_center <= 0.33:
        turn_left("LOW")
    elif 0.34 < x_center < 0.66:
        drive_forward("LOW")
    elif output_data == []:
        stop_robot()

    #ser.write(bytes([left, right]))
    #ser.write(bytes([right, left]))

def act_on_detections(detections, labels):
    for d in detections:
        label = labels[int(d.category)]
        confidence = float(d.conf)
        if label == "person" and confidence > 0.6:
            x, y, w, h = d.box
            x_center = (x + w / 2) / 640
            move_toward_person(x_center)
            return
        else:
            stop_robot()
            return
            

if __name__ == "__main__":
    print("HELLO WORLD")
    camera = IMX500Detector()
    camera.start(show_preview=True)

    print("Running object deteciton with autonomous movement")

    try:
        while True:
            detections = camera.get_detections()
            labels = camera.get_labels()
            
            output_data = []
            for d in detections:
                label = labels[int(d.category)]
                confidence = float(d.conf)
                x, y, w, h = d.box
                
                output_data.append({
                    "label": label,
                    "confidence": confidence,
                    "bbox": {"x": x, "y": y, "w": w, "h": h}
                })
                
            with open("detections.json", "w") as f: 
                json.dump(output_data, f, indent=2)
                
            act_on_detections(detections, labels)
            
            if output_data == []:
                ser.write(bytes([64, 192]))
                
            time.sleep(0.5)
            
        #     try:
        # while True:
        #     detections = camera.get_detections()
        #     labels = camera.get_labels()
            
        #     with open("detections.json", "w") as f: 
        #         json.dump(output_data, f, indent=2)
                
        #     act_on_detections(detections, labels)
            
        #     if output_data == []:
        #         ser.write(bytes([64, 192]))
                
        #     time.sleep(0.5)

    except KeyboardInterrupt:
        print("Shutting down..")
        stop_robot()
        ser.close()
        camera.stop()

