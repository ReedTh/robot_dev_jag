import serial
import time
import pygame

THROTTLE_AXIS = 0
TURN_AXIS = 1 
UPDATE_INTERVAL = 0.01
DEADZONE = 0.1
DEBUG = True


    
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Using Joystick: {joystick.get_name()}")

ser = serial.Serial('/dev/ttyAMA0', 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)

def scale_left(value):
    if abs(value) < DEADZONE:
        return 64
    elif value > 0:
        return int(64 - value * 63)
    else:
        return int(64 - value * 63)

def scale_right(value):
    if abs(value) < DEADZONE:
        return 192
    elif value > 0:
        return int(192 - value * 63)
    else:
        return int(192 - value * 63)

try:
    while True:
        pygame.event.pump()
        
        throttle = joystick.get_axis(THROTTLE_AXIS)
        turn = joystick.get_axis(TURN_AXIS)
        
        if abs(throttle) < DEADZONE:
            throttle = 0.0
        if abs(turn) < DEADZONE:
            turn = 0.0
        
        left = throttle + turn
        right = throttle - turn
        
        left = max(min(left, 1.0), -1.0)
        right = max(min(right, 1.0), -1.0)
        
        left_cmd = scale_left(left)
        right_cmd = scale_right(right)
        
        ser.write(bytes([left_cmd, right_cmd]))
        
        if DEBUG:
            print(f'/r Throttle: {throttle:2f} ~ Turn: {turn:2f} ~ Left Cmd: {left_cmd} ~ Right Cmd: {right_cmd}')
        
        time.sleep(UPDATE_INTERVAL)
except KeyboardInterrupt:
    print("/nStopping Robot...")
    ser.write(bytes([0]))
    joystick.quit()
    pygame.quit()
    ser.close()