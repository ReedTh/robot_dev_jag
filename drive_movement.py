import serial

ser = serial.Serial("/dev/ttyAMA0", 9600)

def drive_forward(speed):
    
    if speed.upper() == "HIGH":
        ser.write(bytes([129, 127]))
    elif speed.upper() == "MID":
        ser.write(bytes([140, 96]))
    elif speed.upper() == "LOW":
        ser.write(bytes([172, 84]))
    else:
        ser.write(bytes([0]))

def drive_backward(speed):
    
    if speed.upper() == "HIGH":
        ser.write(bytes([254, 1]))
    elif speed.upper() == "MID":
        ser.write(bytes([214, 22]))
    elif speed.upper() == "LOW":
        ser.write(bytes([212, 44]))
    else:
        ser.write(bytes([0]))

def turn_right(speed):
    
    if speed.upper() == "MID":
        ser.write(bytes([172, 44]))
def turn_left(speed):
    if speed.upper() == "MID":
        ser.write(bytes([212, 84]))

def stop_robot():
    ser.write(bytes([0]))