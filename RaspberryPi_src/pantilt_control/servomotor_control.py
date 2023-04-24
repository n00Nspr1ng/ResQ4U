import RPi.GPIO as GPIO

class servoMotorController:
    '''
    Class for controlling servo motors.
    Args:
        servomotor: Signal pin number of servo motor. Requires one int.
        delay_time: Delay time (millisec) for step pwm. 1 step runs for 2*(delay_time).
                    Default is set as 1.
    '''
    def __init__(self, servomotor):
        self.current_angle = 90

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servomotor, GPIO.OUT)
        self.servo = GPIO.PWM(servomotor, 50)
        self.servo.start(0)

    def setAngle(self, angle):
        #Something that Dahyun made...
        #Something like this... Molla
        self.servo.ChangeDutyCycle(3.0)

        #Do cut and paste plz