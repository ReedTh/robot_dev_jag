import keyboard
import serial
import time
from drive_movement import drive_backward, drive_forward, turn_left, turn_right

ser = serial.Serial("/dev/ttyAMA0", 9600)

try:
    
    counter = 0
    while True:
        print(f"Heartbeat: {time.time()}")
        
        if keyboard.is_pressed(keyboard.KEY_UP):
            drive_forward("HIGH")
        elif keyboard.is_pressed(keyboard.KEY_DOWN):
            drive_backward("HIGH")
        elif keyboard.is_pressed('Left'):
            turn_left("MID")
        elif keyboard.is_pressed('Right'):
            turn_right("MID")
        else:
            ser.write(bytes([0]))
        
        counter += 1 
except KeyboardInterrupt:
    pass
finally:
    print("done..")