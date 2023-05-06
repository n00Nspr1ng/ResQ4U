# imports (extract to utils file and import at once..)
import argparse
import cv2
import os
from pycoral.adapters.common import input_size
from pycoral.adapters.detect import get_objects
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.edgetpu import run_inference
from serial import Serial
import serial
import RPi.GPIO as GPIO
import time

class HumanDetection:
    def __init__(self, model_path, label_path, top_k=3, threshold=0.1):
        self.model_path = model_path
        self.label_path = label_path
        self.top_k = top_k
        self.threshold = threshold
        self.labels = read_label_file(label_path)
        self.interpreter = make_interpreter(model_path)
        self.interpreter.allocate_tensors()
        self.inference_size = input_size(self.interpreter)

    def is_human_detected(self, cv2_im):
        cv2_im_rgb = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)
        cv2_im_rgb = cv2.resize(cv2_im_rgb, self.inference_size)
        run_inference(self.interpreter, cv2_im_rgb.tobytes())
        objs = get_objects(self.interpreter, self.threshold)[:self.top_k]
        for obj in objs:
            if self.labels[obj.id] == 'person':
                bounding_box = obj.bbox
                bounding_box_center = (
                    int((bounding_box[0] + bounding_box[2]) / 2),
                    int((bounding_box[1] + bounding_box[3]) / 2)
                )
                return True, bounding_box_center
        return False, None

class PanTilt:
    def __init__(self):
        self.frame_center = None
        self.bounding_box_center = None
        
        # pin set up
        self.panPin = 17
        self.tiltPin = 18

        GPIO.setmode(GPIO.BCM)  # use BCM numbering scheme
        GPIO.setup(self.panPin, GPIO.OUT)  # set pan pin as output
        GPIO.setup(self.tiltPin, GPIO.OUT)  # set tilt pin as output

        self.pan = GPIO.PWM(self.panPin, 50)  # 50Hz (PWM frequency)
        self.tilt = GPIO.PWM(self.tiltPin, 50)  # 50Hz

        self.pan.start(0)  # start PWM with 0% duty cycle (servo centered)
        self.tilt.start(0)

    def set_angle(self, angle, pwm):
        duty_cycle = (angle / 18) + 2.5  # convert angle to duty cycle (2.5 - 12.5)
        pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.3)  # give the motor time to move

    def pan_tilt_to_match_frame_center_to_bounding_box_center(self): # used previous algorithm I made..
        error_threshold = 10
        step_size = 5

        error_x = self.frame_center[0] - self.bounding_box_center[0]
        error_y = self.frame_center[1] - self.bounding_box_center[1]

        if (abs(error_x) > error_threshold) or (abs(error_y) > error_threshold):
            if error_x > 0:
                self.pan_angle += step_size
            else:
                self.pan_angle -= step_size
            if error_y > 0:
                self.tilt_angle += step_size
            else:
                self.tilt_angle -= step_size

            self.pan_angle = max(50, min(130, self.pan_angle))
            self.tilt_angle = max(0, min(70, self.tilt_angle))

            self.set_angle(self.pan_angle, self.pan)
            self.set_angle(self.tilt_angle, self.tilt)


class LidarSensor:
    def __init__(self):
        self.tf02_pro = None

    def get_strength_value(self):
        # data type setting (header & uart)
        HEADER = 0x59
        uart = [0] * 9

        # serial setting
        ser = Serial(
            port="/dev/ttyAMA0", # port for LiDAR
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=3
        )

        if ser.in_waiting > 0:
            if ser.readline() == HEADER:
                uart[0] = HEADER

                if ser.readline() == HEADER:
                    uart[1] = HEADER

                    for i in range(2, 9):
                        uart[i] = int.from_bytes(ser.readline(), byteorder='little')
                    check = uart[0] + uart[1] + uart[2] + uart[3] + uart[4] + uart[5] + uart[6] + uart[7]

                    if uart[8] == (check & 0xff):
                        dist = uart[2] + uart[3] * 256
                        strength = uart[4] + uart[5] * 256
                        return strength, dist

    def get_distance_value(self):
        pass


class MotorController:
    def __init__(self, port="/dev/ttyACM0", baudrate=19200): # port for UNO
        self.ser = Serial(port=port, baudrate=baudrate)
        self.off_flag = True
        self.ccw_flag = True

    def send_to_motor_controller(self, distance_value):
        if distance_value >= 15:
            speed = 215
        elif distance_value <= 5:
            speed = 180
        else:
            speed = int(180 + (distance_value - 5) * (215 - 180) / 10)  # linear interpolation (assume that motor speed - distance is linearly correlated)

        self.ser.write(str(speed).encode())
        self.ser.write(b'\n')

    def stop_motors(self):
        if not self.off_flag:
            self.ser.write(b'3\n')  # send mode 3 to toggle motor on/off
            self.off_flag = True


class Robot:
    def __init__(self):
        self.human_detection = HumanDetection(
            model_path='../all_models/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite', # file path would be changed
            label_path='../all_models/coco_labels.txt'
        )
        self.pan_tilt = PanTilt()
        self.lidar_sensor = LidarSensor()
        self.motor_controller = MotorController()

    def run(self):
        threshold = 50  # set threshold value
        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if self.human_detection.is_human_detected(frame):
                self.pan_tilt.frame_center = (frame.shape[1] // 2, frame.shape[0] // 2)
                self.pan_tilt.pan_tilt_to_match_frame_center_to_bounding_box_center()
                distance_values = []
                while True:
                    strength_value, distance_value = self.lidar_sensor.get_strength_value()
                    if strength_value > threshold:
                        distance_values.append(distance_value)
                        if len(distance_values) > 10:
                            average_distance = sum(distance_values) / len(distance_values)
                            self.motor_controller.send_to_motor_controller(average_distance)
                            break
            else:
                self.pan_tilt.bounding_box_center = None
                self.motor_controller.stop_motors()

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
