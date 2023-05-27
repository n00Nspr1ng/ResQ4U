import cv2
import RPi.GPIO as GPIO

# set up GPIO pins for servo motors
panPin   = 18   # GPIO pin for pan servo
tiltPin  = 12   # GPIO pin for tilt servo

GPIO.setmode(GPIO.BCM) # use BCM numbering scheme
GPIO.setup(panPin, GPIO.OUT) # set pan pin as output
GPIO.setup(tiltPin, GPIO.OUT) # set tilt pin as output

# create PWM (for servo)
pan = GPIO.PWM(panPin, 50) # 50Hz (PWM frequency)
tilt = GPIO.PWM(tiltPin, 50) # 50Hz

# start PWM with 0 duty cycle
pan.start(0)
tilt.start(0)

# Camera center point define
center_x = 320 
center_y = 240 

# Pan-tilt angles and control step
pan_angle   = 90
tilt_angle  = 90
pan_step    = 10
tilt_step   = 5

pan_angle_min  = 0
pan_angle_max  = 200
tilt_angle_min = 0
tilt_angle_max = 100

# Threshold error - center & max value
error_threshold = 10

# This would also be changed after mid term
cap = cv2.VideoCapture(0)

# This would also be changed after mid term
# While True -> rectangles (or objs)
while True:
    non, NoiseArr = cap.read()
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(NoiseArr)
    cv2.circle(NoiseArr, max_loc, 10, (0, 0, 255), 2)

    # Calculate the error between the center and the maximum value
    error_x = center_x - max_loc[0]
    error_y = center_y - max_loc[1]

    if abs(error_x) > error_threshold or abs(error_y) > error_threshold:
        if error_x > 0:
            pan_angle += pan_step
        if error_x < 0:
            pan_angle -= pan_step

        if error_y > 0:
            tilt_angle += tilt_step
        else: # error_y < 0
            tilt_angle -= tilt_step
        
        # Pan angle limitation to [pan_angle_min, pan_angle_max]
        pan_angle = max(pan_angle_min, min(pan_angle_max, pan_angle))
        # Limit the tilt angle to [tilt_angle_min, tilt_angle_max]
        tilt_angle = max(tilt_angle_min, min(tilt_angle_max, tilt_angle))

		# move the pan-tilt camera to track the face
		setAngle(pan_angle, pan)
		setAngle(tilt_angle, tilt)


    cv2.imshow('frame', cv2_im)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
