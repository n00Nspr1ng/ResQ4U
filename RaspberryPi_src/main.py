import sys
sys.path.append('/home/roboin/ResQ4U/RaspberryPi_src/common')
from imports import *

from pan_tilt.pan_tilt import PanTilt
from serial_communication.arduino_serial import SerialWrapper
from camera_detection.detect_person_v2 import PersonDetector
from pan_tilt.stepmotor_control import StepMotorController
from alert.relay_control import Relay



if __name__ == "__main__":
    print('Hello ResQ4U')

    # inits
    pan_tilt = PanTilt(config)
    arduino = SerialWrapper(device=config.arduino_uno)
    detector = PersonDetector(pan_tilt, show_image=True)
    searchLight = Relay(pin = config.searchlight)
    alertLight = Relay(pin = config.alert)

    # Turn Search Light OFF
    searchLight.off()
    print('Searchlight OFF ...')

    # Turn Alert Siren OFF
    alertLight.off()
    print('Alert OFF ...')

    # DETECT
    while True:
        mode = detector.detect()
        print("mode", mode)
        if (mode == 0): 
            print("inside mode 0")
            arduino.send_flag("d")
            time.sleep(0.5)
        elif (mode == 1):
            print("inside mode 1")
            break
    
    time.sleep(1)
    arduino.send_flag("a")
    
    ###################### WHEN DETECTED LAUNCH! #######################
    # Call for HELP
    # caller.callHELP() -- test this at last (SID authorization shouldnt be on git public)

    # Turn Search Light ON
    searchLight.on()
    print('Searchlight ON ...')
    
    # Turn Alert Siren ON
    alertLight.on()
    print('Alert ON ...')

    # Read Arduino
    while(arduino.end_flag == False):
        arduino.check_end_flag()
    
    # #################### AFTER LAUNHCH RETURN INIT ####################
    
    print("END ... Returning to initial state ...")
    
    # PanTilt to initial State
    pan_tilt.return_to_init()
    
    # Turn Search Light OFF
    searchLight.off()
    print('Searchlight OFF ...')

    # Turn Alert Siren OFF
    alertLight.off()
    print('Alert OFF ...')





# from camera_detection.detect_person import PersonDetector