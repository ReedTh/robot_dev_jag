"""This is a function that makes it easier to work wiht the sabertooth motordriver"""

def speed_to_command(motor: int, speed: float) -> int:
    """
    Convert a normalized speed (-1.0 to 1.0) to a Saber tooth Simplified Serial Commmand.
    
    motor: 1 or 2
    speed: float between -1.0 (Full reverse) and 1.0 (Full forward)
    
    returns: int command 0-255
    """
    MOTOR1_STOP, MOTOR1_MAX = 64, 127
    MOTOR2_STOP, MOTOR2_MAX = 192, 255

    #Clamp speed 
    speed = max(-1.0, min(1.0, speed))

    if motor == 1:
        return int(round(MOTOR1_STOP + speed * (MOTOR1_MAX - MOTOR1_STOP)))
    elif motor == 2:
        return int(round(MOTOR2_STOP - speed * (MOTOR2_MAX - MOTOR2_STOP)))
    else:
        raise ValueError("Motor must be 1 or 2")
