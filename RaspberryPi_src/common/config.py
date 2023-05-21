from dataclasses import dataclass

# Arduino port number
@dataclass
class arduino_uno:
    port = "/dev/ttyACM0"
    baudrate = 9600

# Step motor for pan, set up as GPIO.BCM
@dataclass
class pan_motor:
    STEP : int = 24
    DIR : int = 23

@dataclass
class tilt_motor:
    STEP : int = 20
    DIR : int = 16

# Servo motor for tilt, set up as GPIO.BCM
servomotor : int = 25

searchlight : int = 17
alert : int = 26