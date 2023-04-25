# PSEUDO CODE WRITTEN BY DAHYUN
# PAN TILT BY 2 STEPPING MOTORS


# IMPORTS
import RPi.GPIO as GPIO
import time

# Class
class PanTilt_STEP:
    # Initialize the class with the pins and steps per revolution
    def __init__(self, pan_step, pan_dir, tilt_step, tilt_dir, pan_steps_per_rev, tilt_steps_per_rev):
        # Set the GPIO mode
        GPIO.setmode(GPIO.BCM)
        # Set the pins as attributes
        self.pan_step = pan_step
        self.pan_dir = pan_dir
        self.tilt_step = tilt_step
        self.tilt_dir = tilt_dir
        # Set the steps per revolution as attributes
        self.pan_steps_per_rev = pan_steps_per_rev
        self.tilt_steps_per_rev = tilt_steps_per_rev
        # Set the pins as outputs
        GPIO.setup(self.pan_step, GPIO.OUT)
        GPIO.setup(self.pan_dir, GPIO.OUT)
        GPIO.setup(self.tilt_step, GPIO.OUT)
        GPIO.setup(self.tilt_dir, GPIO.OUT)
        # Define the delay between each step
        self.delay = 0.01

    # PAN
    def pan(self, angle):
        # Calculate number of steps to move
        steps = int(angle * self.pan_steps_per_rev / 360)
        # Set direction
        if angle > 0:
            GPIO.output(self.pan_dir, GPIO.HIGH)
        else:
            GPIO.output(self.pan_dir, GPIO.LOW)
        # Loop through steps
        for i in range(steps):
            # Turn on pan step pin
            GPIO.output(self.pan_step, GPIO.HIGH)
            # time sleep
            time.sleep(self.delay)
            # Turn off pan step pin
            GPIO.output(self.pan_step, GPIO.LOW)
            # time sleep
            time.sleep(self.delay)

    # TILT
    def tilt(self, angle):
        # Calculate number of steps to move
        steps = int(angle * self.tilt_steps_per_rev / 360)
        # Set direction
        if angle > 0:
            GPIO.output(self.tilt_dir, GPIO.HIGH)
        else:
            GPIO.output(self.tilt_dir, GPIO.LOW)
        # Loop through steps
        for i in range(steps):
            # Turn on tilt step pin
            GPIO.output(self.tilt_step, GPIO.HIGH)
            # time sleep
            time.sleep(self.delay)
            # Turn off tilt step pin
            GPIO.output(self.tilt_step, GPIO.LOW)
            # time sleep
            time.sleep(self.delay)

    # Define a method to clean up the GPIO pins and exit
    def cleanup(self):
        GPIO.cleanup()
