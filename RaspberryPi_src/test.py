#!/usr/bin/env python3

import serial
import time
from common import config

#from pantilt_control.stepmotor_control import stepMotorController
#from common.config import stepmotor

from serial_communication.arduino_serial import SerialWrapper

if __name__ == "__main__":
    # try: 
    #     arduino = serial.Serial(config.arduino_uno.port, config.arduino_uno.baudrate, timeout=1)
    #     arduino.reset_input_buffer()

    #     arduino.isOpen()
    #     print(arduino.name)
    # except:
    #     print("Error")

    # while True:
    #     if arduino.in_waiting > 0:
    #         line = arduino.readline().decode('utf-8').rstrip()
    #         print(line)

    arduino = SerialWrapper(config.arduino_uno)
    while True:
        print("Sending detect_flag")
        arduino.send_flag("detect")
        time.sleep(0.2)
    
        print("Sending align flag")
        arduino.send_flag("align")
        time.sleep(0.2)

    # stepMotor = stepMotorController(stepmotor=stepmotor)
    # stepMotor.move(step=250, dir=0)
    # stepMotor.return_init()