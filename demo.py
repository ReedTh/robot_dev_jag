from ai_camera import IMX500Detector, Detection
import time

camera = IMX500Detector()

camera.start(show_preview=True)

try:
    while True:
        detections = camera.get_detections()
        
        if detections:
            for detection in detections:
                label = detection.category
                confidence = detection.conf
                print(f"Detected {label} with confidence {confidence:.2f}")
        else:
            print("No objects detected")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Stopping..")
    camera.stop()
  
  