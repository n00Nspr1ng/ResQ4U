#!/usr/bin/env python3

import serial
import time
from common import config

from motor_control.stepmotor_control import StepMotorController
#from common.config import stepmotor

from serial_communication.arduino_serial import SerialWrapper

if __name__ == "__main__":

    arduino = SerialWrapper(device=config.arduino_uno)

    print("sending flag f")
    arduino.send_flag("f")
    while(arduino.end_flag == False):
        arduino.check_end_flag()
    print("rasp ended")

    # panMotor = StepMotorController(config.pan_motor, gear_ratio=4)
    # tiltMotor = StepMotorController(config.tilt_motor, gear_ratio=2)
    
    # time.sleep(2)
    # for i in range(20):
    #     panMotor.move(angle=1, ccw_dir=-1)
    #     tiltMotor.move(angle=1, ccw_dir=-1)
    # time.sleep(0.2)

    # panMotor.return_to_initial()
    # tiltMotor.return_to_initial()

    #time.sleep(0.2)
    #for i in range(15):
    #    panMotor.move(angle=1, ccw_dir=-1)
    #    tiltMotor.move(angle=1, ccw_dir=-1)
    #time.sleep(0.2)

    #panMotor.return_to_initial()
    #tiltMotor.return_to_initial()
    
    # time.sleep(1)
    # panMotor.move(angle=30, dir=1)
    # time.sleep(0.2)
    # panMotor.return_to_initial()