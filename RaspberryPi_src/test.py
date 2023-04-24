#!/usr/bin/env python3

#import serial
#from common import config

from pantilt_control.stepmotor_control import stepMotorController
from common.config import stepmotor


if __name__ == "__main__":
    # arduino = serial.Serial(config.ardu_device, 9600, timeout=1)
    # arduino.reset_input_buffer()

    # while True:
    #     if arduino.in_waiting > 0:
    #         line = arduino.readline().decode('utf-8').rstrip()
    #         print(line)

    stepMotor = stepMotorController(stepmotor=stepmotor)
    stepMotor.move(step=250, dir=0)
    stepMotor.return_init()