import sys
sys.path.append('/home/roboin/ResQ4U/RaspberryPi_src/common')
from imports import *

from pan_tilt.pan_tilt import PanTilt
from serial_communication.arduino_serial import SerialWrapper
from camera_detection.detect_person import PersonDetector
from pan_tilt.stepmotor_control import StepMotorController
from alert.relay_control import Relay



if __name__ == "__main__":
    print('Hello ResQ4U')

    pan_tilt = PanTilt(config)
    arduino = SerialWrapper(device=config.arduino_uno)
    detector = PersonDetector(pan_tilt, arduino, show_image=True)
    detector.detect()
    
    # if detector.is_detected:
    #     arduino.send_flag("d") # detected
    #     pan_tilt.pan_tilt([detector.xc, detector.yc])
    #     if pan_tilt.align_flag == True:
    #         arduino.send_flag("a")


    # caller.callHELP() -- test this at last (SID authorization shouldnt be on git public)

    searchLight=Relay(pin = config.searchlight)
    searchLight.on()
    print('Searchlight ON ...')
    alertLight = Relay(pin = config.alert)
    alertLight.on()
    print('Alert ON ...')

    while(arduino.end_flag == False):
        arduino.check_end_flag()
        print(arduino.read_line())
    
    print("END ... Returning to initial state ...")
    
    pan_tilt.return_to_init()
    
