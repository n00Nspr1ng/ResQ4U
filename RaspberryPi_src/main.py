import sys
sys.path.append('/home/roboin/ResQ4U/RaspberryPi_src/common')
from imports import *

from pan_tilt.pan_tilt import PanTilt
from serial_communication.arduino_serial import SerialWrapper
from camera_detection.detect_person import PersonDetector
from pan_tilt.stepmotor_control import StepMotorController
# from alert.relay_control import Relay

# from camera_detection.camera_test import PersonDetector

if __name__ == "__main__":

    # arduino = SerialWrapper(device=config.arduino_uno)

    # print("sending flag f")
    # arduino.send_flag("f")
    # while(arduino.end_flag == False):
    #     arduino.check_end_flag()
    # print("rasp ended")

    # panMotor = StepMotorController(config.pan_motor, gear_ratio=4)
    # tiltMotor = StepMotorController(config.tilt_motor, gear_ratio=2)
    
    # time.sleep(2)
    # for i in range(60):
    #     panMotor.move(angle=0.45, ccw_dir=1)
    #     tiltMotor.move(angle=0.45, ccw_dir=1)
    # time.sleep(0.2)

    # panMotor.return_to_initial()
    # tiltMotor.return_to_initial()

    # time.sleep(0.2)
    # for i in range(15):
    #    panMotor.move(angle=0.45, ccw_dir=0)
    #    tiltMotor.move(angle=0.45, ccw_dir=0)
    # time.sleep(0.2)

    # panMotor.return_to_initial()
    # tiltMotor.return_to_initial()
    
    # time.sleep(1)
    # panMotor.move(angle=30, dir=1)
    # time.sleep(0.2)
    # panMotor.return_to_initial()
    

    # pan_tilt = PanTilt(config)
    # pan_tilt.pan_tilt([300, 200])

    print('hello')
    pan_tilt = PanTilt(config)
    arduino = SerialWrapper(device=config.arduino_uno)
    detector = PersonDetector(pan_tilt, arduino, show_image)
    # # 
    detector.detect()
    
    # caller.callHELP()
    
    # relay.on(config.searchlight)
    # print('searchlight ON')
    # relay.on(config.alert)
    # print('alert ON')

    # arduino.send_flag("d")
    # time.sleep(5)
    # arduino.send_flag("a")

    while(arduino.end_flag == False):
        arduino.check_end_flag()
        #print(arduino.read_line())
    print("end. returning to initial")
    
    pan_tilt.return_to_init()
    
