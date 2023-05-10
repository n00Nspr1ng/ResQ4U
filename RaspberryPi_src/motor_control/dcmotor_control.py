import RPi.GPIO as GPIO
import time

class StepMotorController:
    '''
    Class for controlling step motors.
    Args:
        stepmotor: Pin numbers of step motor. Requires @dataclass of STEP and DIR.
        delay_time: Delay time (sec) for step pwm. 1 step runs for 2*(delay_time).
                    Default is set as 1.
        gear_ratio: Gear ratio used for step motor.
    '''
    def __init__(self, stepmotor, delay_time=0.001, gear_ratio):
        
        self.STEP = stepmotor.STEP
        self.DIR = stepmotor.DIR
        self.delay_time = delay_time
        self.current_angle = 90
        self.gear_ratio = gear_ratio
        self.angle_per_step = 1.8/16

        # Setup for GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.setup(self.STEP, GPIO.OUT)
        
        
    def move(self, step, dir):
        # Set direction
        # 0 -> CW(+), 1-> CCW(-)
        GPIO.output(self.DIR, dir)
        # Move step 
        for i in range(step):
            GPIO.output(self.STEP, GPIO.HIGH)
            time.sleep(self.delay_time)
            GPIO.output(self.STEP, GPIO.LOW)
            time.sleep(self.delay_time)
        if (dir == 0):
            self.current_angle += step*self.angle_per_step
        else:
            self.current_angle -= step*self.angle_per_step
        print("angle =", self.current_angle)


    def return_to_initial(self):
        angle = self.current_angle - 90
        step = int(angle/self.angle_per_step)
        if (step > 0):
            self.move(step, 1) # move back ccw
        else:
            self.move(step, 0) # move back cw


    def get_angle(self): # Erase if not used
        return self.current_angle
