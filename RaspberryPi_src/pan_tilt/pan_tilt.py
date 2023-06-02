import sys
sys.path.append('/home/roboin/ResQ4U/RaspberryPi_src/common')
from imports import *
from .stepmotor_control import StepMotorController


class PanTilt:
    def __init__(self, config):
        # self.frame_center = [960,540] # 1080p
        self.frame_center = [640,360] # 720p
        # self.frame_center = [320,240] # 480p
        #self.bounding_box_center = None
        
        self.panMotor = StepMotorController(config.pan_motor, gear_ratio=4)
        self.tiltMotor = StepMotorController(config.tilt_motor, gear_ratio=2)

        self.pan_step : int = 0
        self.tilt_step : int = 0

        self.align_flag : bool = False
        self.count = 0
        

    def pan_tilt(self, bounding_box_center):
        
        error_threshold =  10   # theoretically this should be smaller than 5 (cause align delta is 10...)

        pan_step   : int = 4  # changed due to framerate (*should be multiple of 1.8)
        tilt_step  : int = 4

        if bounding_box_center is not None:
            print("frame:", self.frame_center, "bbox:", bounding_box_center)
            error_x = self.frame_center[0] - bounding_box_center[0]
            error_y = - self.frame_center[1] + bounding_box_center[1]

            if (abs(error_x) > error_threshold) or (abs(error_y) > error_threshold):
                self.align_flag = False
                self.count = 0

                if error_x > 0:
                    self.panMotor.move_v2(step=pan_step, ccw_dir=0)
                    self.pan_step += pan_step
                else:
                    self.panMotor.move_v2(step=pan_step, ccw_dir=1)
                    self.pan_step -= pan_step
                if error_y > 0:
                    self.tiltMotor.move_v2(step=tilt_step, ccw_dir=0)
                    self.tilt_step += tilt_step
                else:
                    self.tiltMotor.move_v2(step=tilt_step, ccw_dir=1)
                    self.tilt_step -= tilt_step

                print("pan step:", self.pan_step, " tilt step:", self.tilt_step)
                
            else:
                self.count += 1
                if (self.count == 10):
                    self.align_flag = True
                    print("align done")
        else :
            print('self.bounding box center is NONE')
            

    def return_to_init(self):
        self.panMotor.return_to_initial2()
        self.tiltMotor.return_to_initial2()
