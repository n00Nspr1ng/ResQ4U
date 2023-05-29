#from common.imports import *
from .stepmotor_control import StepMotorController


class PanTilt:
    def __init__(self, config):
        self.cap = cv2.VideoCapture(0)
        self.frame_center = None
        
        #self.bounding_box_center = None
        
        self.panMotor = StepMotorController(config.pan_motor, gear_ratio=4)
        self.tiltMotor = StepMotorController(config.tilt_motor, gear_ratio=2)

        self.pan_angle = 0
        self.tilt_angle = 0

        self.align_flag : bool = False
        self.count = 0
        
    def detect_frame_center(self):
        ret1, frame1 = self.cap.read()
        if not ret1:
            return
        frame_height, frame_width = frame1.shape[:2]
        self.frame_center = [int(frame_width/2), int(frame_height/2)]
        

    def pan_tilt(self, bounding_box_center): # used previous algorithm I made..
        
        error_threshold =  10
        pan_step        =  0.45
        tilt_step       =  0.45

        if bounding_box_center is not None:
            print("frame:", self.frame_center, "bbox:", bounding_box_center)
            error_x = self.frame_center[0] - bounding_box_center[0]
            error_y = - self.frame_center[1] + bounding_box_center[1]

            if (abs(error_x) > error_threshold) or (abs(error_y) > error_threshold):
                self.align_flag = False
                self.count = 0

                if error_x > 0:
                    self.panMotor.move(angle=pan_step, ccw_dir=0)
                    self.pan_angle += pan_step
                    #pan_dir = 0
                else:
                    self.panMotor.move(angle=pan_step, ccw_dir=1)
                    self.pan_angle -= pan_step
                    #pan_dir = 1
                if error_y > 0:
                    self.tiltMotor.move(angle=tilt_step, ccw_dir=0)
                    self.tilt_angle += tilt_step
                    #tilt_dir = 0
                else:
                    self.tiltMotor.move(angle=tilt_step, ccw_dir=1)
                    self.tilt_angle -= tilt_step
                    #tilt_dir = 1

                #self.pan_angle = max(-50, min(50, self.pan_angle))
                #self.tilt_angle = max(-35, min(35, self.tilt_angle))

                print("pan=", self.pan_angle, "tilt=", self.tilt_angle)

                #self.panMotor.move(angle=self.pan_angle, ccw_dir=pan_dir)
                #self.tiltMotor.move(angle=self.tilt_angle, ccw_dir=tilt_dir)
                
            else:
                self.count += 1
                if (self.count == 20):
                    self.align_flag = True
        else :
            print('self.bounding box center is NONE')
            

    def return_to_init(self):
        self.panMotor.return_to_initial()
        self.tiltMotor.return_to_initial()
