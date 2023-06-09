import sys
sys.path.append('/home/roboin/ResQ4U/RaspberryPi_src/common')
from imports import *

class StepMotorController:
    '''
    Class for controlling step motors.
    Args:
        stepmotor: Pin numbers of step motor. Requires @dataclass of STEP and DIR.
        gear_ratio: Gear ratio used for step motor.
        delay_time: Delay time (sec) for step pwm. 1 step runs for 2*(delay_time).
                    Default is set as 1.
    '''
    def __init__(self, stepmotor, gear_ratio, delay_time=0.001):
        
        self.STEP = stepmotor.STEP
        self.DIR = stepmotor.DIR
        self.delay_time = delay_time
        self.gear_ratio = gear_ratio
        self.angle_per_step = 1.8/16

        self.current_angle = 0
        self.current_step = 0

        # Setup for GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.setup(self.STEP, GPIO.OUT)
    

    def move(self, angle, ccw_dir):
        # Note that this "angle" is difference between current angle and desired angle
        step = int(angle / self.angle_per_step * self.gear_ratio)
        #print("moving")
        #print("steps to move", step)

        # Set direction
        # 0 -> CW, 1-> CCW
        GPIO.output(self.DIR, ccw_dir)

        # Move step 
        for i in range(step):
            GPIO.output(self.STEP, GPIO.HIGH)
            time.sleep(self.delay_time)
            GPIO.output(self.STEP, GPIO.LOW)
            time.sleep(self.delay_time)
        if (ccw_dir == 0):
            self.current_angle += angle
        else:
            self.current_angle -= angle
        #print("current angle of step motor = ", self.current_angle)
        

    def move_v2(self, step, ccw_dir): #DEPRECATED
        # Set direction
        # 0 -> CW(+), 1-> CCW(-)
        GPIO.output(self.DIR, ccw_dir)

        # Move step 
        for i in range(step):
            GPIO.output(self.STEP, GPIO.HIGH)
            time.sleep(self.delay_time)
            GPIO.output(self.STEP, GPIO.LOW)
            time.sleep(self.delay_time)
        if (ccw_dir == 0):
            self.current_step += step
        else:
            self.current_step -= step
        # print("step =", self.current_step)


    def return_to_initial(self):
        angle = self.current_angle
        print(angle)
        if (angle > 0):
            self.move(angle, 1) # move back ccw
            print("1")
        else:
            self.move(-angle, 0) # move back cw
            print("0")

    def return_to_initial2(self):
        step = self.current_step
        print(step)
        if (step > 0):
            self.move_v2(step, 1) # move back ccw
            print("1")
        else:
            self.move_v2(-step, 0) # move back cw
            print("0")    


    def get_angle(self): # Erase if not used
        return self.current_angle
