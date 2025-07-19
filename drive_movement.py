import serial
from serial_sabertooth_trans import speed_to_command

ser = serial.Serial("/dev/ttyAMA0", 9600)



def drive_forward(speed):
    
    if speed.upper() == "HIGH":
        ser.write(bytes([speed_to_command(1,1.0), speed_to_command(2,1.0)]))
    elif speed.upper() == "MID":
        ser.write(bytes([speed_to_command(1,0.66), speed_to_command(2,0.66)]))
    elif speed.upper() == "LOW":
        ser.write(bytes([speed_to_command(1,0.33), speed_to_command(2,0.33)]))
    else:
        ser.write(bytes([0]))


def drive_backward(speed):
    
    if speed.upper() == "HIGH":
        ser.write(bytes([speed_to_command(1,-1.0), speed_to_command(2,-1.0)]))
    elif speed.upper() == "MID":
        ser.write(bytes([speed_to_command(1,-0.66), speed_to_command(2,-0.66)]))
    elif speed.upper() == "LOW":
        ser.write(bytes([speed_to_command(1,-0.33), speed_to_command(2,-0.33)]))
    else:
        ser.write(bytes([0]))


def turn_right(speed):
    
    if speed.upper() == "HIGH":
        ser.write(bytes([speed_to_command(1,-1.0), speed_to_command(2,1.0)]))
    elif speed.upper() == "MID":
        ser.write(bytes([speed_to_command(1,-0.66), speed_to_command(2,0.66)]))
    elif speed.upper() == "LOW":
        ser.write(bytes([speed_to_command(1,-0.33), speed_to_command(2,0.33)]))
    else:
        ser.write(bytes([0]))


def turn_left(speed):
    if speed.upper() == "HIGH":
        ser.write(bytes([speed_to_command(1,1.0), speed_to_command(2,-1.0)]))
    elif speed.upper() == "MID":
        ser.write(bytes([speed_to_command(1,0.66), speed_to_command(2,-0.66)]))
    elif speed.upper() == "LOW":
        ser.write(bytes([speed_to_command(1,0.33), speed_to_command(2,-0.33)]))
    else:
        ser.write(bytes([0]))

def strafe_FL(speed):
    pass

def strafe_FR(speed):
    pass

def strafe_RL(speed):
    pass

def strafe_RR(speed):
    pass

def stop_robot():
    ser.write(bytes([0]))