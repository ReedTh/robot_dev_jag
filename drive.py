 import serial 
from serial_sabertooth_trans import speed_to_command

class Controller:
    def __init__(self):
        self.ser = serial.Serial("dev/tty/AMA0")

    
    def drive_forward(self, speed):
    
        if speed.upper() == "HIGH":
            self.ser.write(bytes([speed_to_command(1,1.0), speed_to_command(2,1.0)]))
        elif speed.upper() == "MID":
            self.ser.write(bytes([speed_to_command(1,0.66), speed_to_command(2,0.66)]))
        elif speed.upper() == "LOW":
            self.ser.write(bytes([speed_to_command(1,0.33), speed_to_command(2,0.33)]))
        else:
            self.ser.write(bytes([0]))


    def drive_backward(self, speed):
        
        if speed.upper() == "HIGH":
            self.ser.write(bytes([speed_to_command(1,-1.0), speed_to_command(2,-1.0)]))
        elif speed.upper() == "MID":
            self.ser.write(bytes([speed_to_command(1,-0.66), speed_to_command(2,-0.66)]))
        elif speed.upper() == "LOW":
            self.ser.write(bytes([speed_to_command(1,-0.33), speed_to_command(2,-0.33)]))
        else:
            self.ser.write(bytes([0]))


    def turn_right(self, speed):
        
        if speed.upper() == "HIGH":
            self.ser.write(bytes([speed_to_command(1,-1.0), speed_to_command(2,1.0)]))
        elif speed.upper() == "MID":
            self.ser.write(bytes([speed_to_command(1,-0.66), speed_to_command(2,0.66)]))
        elif speed.upper() == "LOW":
            self.ser.write(bytes([speed_to_command(1,-0.33), speed_to_command(2,0.33)]))
        else:
            self.ser.write(bytes([0]))


    def turn_left(self, speed):
        if speed.upper() == "HIGH":
            self.ser.write(bytes([speed_to_command(1,1.0), speed_to_command(2,-1.0)]))
        elif speed.upper() == "MID":
            self.ser.write(bytes([speed_to_command(1,0.66), speed_to_command(2,-0.66)]))
        elif speed.upper() == "LOW":
            self.ser.write(bytes([speed_to_command(1,0.33), speed_to_command(2,-0.33)]))
        else:
            self.ser.write(bytes([0]))
