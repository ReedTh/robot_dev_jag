import keyboard
import serial
import time
from drive_movement import drive_backward, drive_forward, turn_left, turn_right, strafe_FL, strafe_FR, strafe_RL, strafe_RR

ser = serial.Serial("/dev/ttyAMA0", 9600)

# initalized the mode
motor_drive_speed_d = {1:"LOW",
                       2:"MID",
                       3:"HIGH"}
mode_drive_speed = 1

try:
    
    while True:
        
        # Mode Dectector 
        if keyboard.is_pressed('1'):
            mode_drive_speed = 1
        elif keyboard.is_pressed('2'):
            mode_drive_speed = 2
        elif keyboard.is_pressed('3'):
            mode_drive_speed = 3


        #print(f"Heartbeat: {time.time()}")
        

        if keyboard.is_pressed(keyboard.KEY_UP):
            drive_forward(motor_drive_speed_d[mode_drive_speed])
        elif keyboard.is_pressed(keyboard.KEY_DOWN):
            drive_backward(motor_drive_speed_d[mode_drive_speed])
        elif keyboard.is_pressed('Left'):
            turn_left(motor_drive_speed_d[mode_drive_speed])
        elif keyboard.is_pressed('Right'):
            turn_right(motor_drive_speed_d[mode_drive_speed])


        # elif keyboard.is_pressed('Left') & keyboard.is_pressed(keyboard.KEY_UP):
        #     strafe_FL(motor_drive_speed_d[mode_drive_speed])
        # elif keyboard.is_pressed('Right') & keyboard.is_pressed(keyboard.KEY_UP):
        #     strafe_FR(motor_drive_speed_d[mode_drive_speed])
        # elif keyboard.is_pressed('Left') and keyboard.is_pressed(keyboard.KEY_DOWN):
        #     strafe_RR(motor_drive_speed_d[mode_drive_speed])
        # elif keyboard.is_pressed('Right') and keyboard.is_pressed(keyboard.KEY_DOWN):
        #     strafe_RL(motor_drive_speed_d[mode_drive_speed])

            
        else:
            ser.write(bytes([0]))
        
except KeyboardInterrupt:
    pass
finally:
    print("done..")