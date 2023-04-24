from common.config import stepmotor
import RPi.GPIO as GPIO
import time

class stepMotorController:
    '''
    Class for controlling step motors.
    Args:
        stepmotor: Pin numbers of step motor. Requires @dataclass of STEP and DIR.
        delay_time: Delay time (millisec) for step pwm. 1 step runs for 2*(delay_time).
                    Default is set as 1.
    '''
    def __init__(self, stepmotor, delay_time=1):
        # Setup for GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(stepmotor.DIR, GPIO.OUT)
        GPIO.setup(stepmotor.STEP, GPIO.OUT)

        self.delay_time = delay_time
        self.current_angle = 90
        self.angle_per_step = 1.8/16
        
    def move(self, step, dir):
        # Set direction
        # 0 -> CW(+), 1-> CCW(-)
        GPIO.output(stepmotor.DIR, dir)
        # Move step 
        for i in range(step):
            GPIO.output(stepmotor.STEP, GPIO.HIGH)
            time.sleep(self.delay_time/(1e3))
            GPIO.output(stepmotor.STEP, GPIO.LOW)
            time.sleep(self.delay_time/(1e3))
        if (dir == 0):
            self.current_angle += step*self.angle_per_step
        else:
            self.current_angle -= step*self.angle_per_step
        print("angle =", self.current_angle)

    def return_init(self):
        angle = self.current_angle - 90
        step = int(angle/self.angle_per_step)
        if (step > 0):
            self.move(step, 1) # move back ccw
        else:
            self.move(step, 0) # move back cw

    def get_angle(self): # Erase if not used
        return self.current_angle
