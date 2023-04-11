#!/usr/bin/env python3

import serial

from common.config import ardu_device

if __name__ == "__main__":
    arduino = serial.Serial(ardu_device, 9600, timeout=1)
    arduino.reset_input_buffer()


    while True:
        if arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8').rstrip()
            print(line)