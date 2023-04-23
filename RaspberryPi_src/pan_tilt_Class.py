##########################################################################
#        READ ME !
#        CODE BY DAHYUN
#        DIDNT HAVE TIME TO TEST
#        CODE WILL BE MODIFIED AS SOON AS MY MID TERM IS OVER !
#        I WILL MAKE THESE (DETECTION + LIDAR + PAN TILT) CODES TO CLASSES.. 
#        HAVE A GREAT DAY FOR THOSE WHO ARE READING THIS.......
###########################################################################

class PanTilt:
    def __init__(self):
        # Camera center pixels > (Dahyun will change this code after mid term..)
        center_x = 320
        center_y = 240
        
        # Pan-tilt angles and control step
        self.pan_angle = 90
        self.tilt_angle = 90
        self.step_size = 5
        
        # Threshold error - center & max value
        self.error_threshold = 10
        
        GPIO.setmode(GPIO.BCM) # use BCM numbering scheme
        GPIO.setup(panPin, GPIO.OUT) # set pan pin as output
        GPIO.setup(tiltPin, GPIO.OUT) # set tilt pin as output

        # create PWM (for servo)
        pan = GPIO.PWM(panPin, 50) # 50Hz (PWM frequency)
        tilt = GPIO.PWM(tiltPin, 50) # 50Hz

        
    def MotorController(self, pan_angle, tilt_angle) :
      # move the pan-tilt camera to track the face
      setAngle(pan_angle, pan)
      setAngle(tilt_angle, tilt)


    def Move2Target(self, camera_fame):
        NoiseArr = camera_fame
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(NoiseArr)
        cv2.circle(NoiseArr, max_loc, 10, (0, 0, 255), 2)

        # Calculate the error between the center and the maximum value
        error_x = self.center_x - max_loc[0]
        error_y = self.center_y - max_loc[1]

        if (abs(error_x) > self.error_threshold) or (abs(error_y) > self.error_threshold):
            if error_x > 0:
                pan_angle += self.step_size
            else:
                pan_angle -= self.step_size
            if error_y > 0:
                tilt_angle += self.step_size
            else:
                tilt_angle -= self.step_size

            # Pan angle limitation to [50, 130]
            pan_angle = max(50, min(130, pan_angle))
            # Limit the tilt angle to [0, 70]
            tilt_angle = max(0, min(70, tilt_angle))

            
if __name__=="__main__":
    Pantilt = PanTilt()
    Pantilt.MotorController(70,70)
#     Pantilt.Move2Target()
