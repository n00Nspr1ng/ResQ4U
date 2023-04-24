from dataclasses import dataclass

# Arduino port number
ardu_device = "/dev/ttyACM0"

# Step motor for pan, set up as GPIO.BCM
@dataclass
class stepmotor:
    STEP : int = 24
    DIR : int = 23

# Servo motor for tilt, set up as GPIO.BCM
servomotor : int = 25