import json
import time
import serial 
from ai_camera import IMX500Detector


ser = serial.Serial("/dev/ttyAMA0", 9600)
LEFT_ZERO = 64
RIGHT_ZERO = 192


def move_forward(power=15):
    left = 64 - power
    right = 192 - power
    ser.write(bytes([left, right]))
        
def stop():
    ser.write(bytes([LEFT_ZERO, RIGHT_ZERO]))

def move_toward_person(x_center, power=15):

    if x_center < 0.4:
        left = 64 + int(power / 2)
        right = 192 - power
    elif x_center > 0.6:
        left = 64 - power
        right = 192 + int(power / 2)
    elif 0.4 < x_center < 0.6:
        left = 64 - power
        right = 192 - power
    elif output_data == []:
        left = 64
        right = 192
        
        ser.write(bytes([left, right]))

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
            stop()
            return
            

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

except KeyboardInterrupt:
    print("Shutting down..")
    stop()
    ser.close()
    camera.stop()

