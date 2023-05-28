from common.imports import *
from motor_control.stepmotor_control import StepMotorController

class PanTilt:
    def __init__(self):
        self.frame_center = None
        self.bounding_box_center = None
        
        self.panMotor = StepMotorController(config.pan_motor, gear_ratio=4)
        self.tiltMotor = StepMotorController(config.tilt_motor, gear_ratio=2)

        self.panMotor.return_to_initial()
        self.tiltMotor.return_to_initial()


    def pan_tilt_to_match_frame_center_to_bounding_box_center(self): # used previous algorithm I made..
        
        error_threshold =  1
        pan_step        = 15
        tilt_step       =  5

        if self.bounding_box_center is not None:
            error_x = self.frame_center[0] - self.bounding_box_center[0]
            error_y = self.frame_center[1] - self.bounding_box_center[1]

            if (abs(error_x) > error_threshold) or (abs(error_y) > error_threshold):
                if error_x > 0:
                    self.pan_angle += pan_step
                else:
                    self.pan_angle -= pan_step
                if error_y > 0:
                    self.tilt_angle += tilt_step
                else:
                    self.tilt_angle -= tilt_step

                self.pan_angle = max(50, min(130, self.pan_angle))
                self.tilt_angle = max(0, min(70, self.tilt_angle))

                self.panMotor.move(angle=self.pan_angle, ccw_dir=-1)
                self.tiltMotor.move(angle=self.tilt_angle, ccw_dir=-1)
        else :
            print('self.bounding box center is NONE')