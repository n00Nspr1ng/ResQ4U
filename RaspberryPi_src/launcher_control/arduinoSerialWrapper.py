#!/usr/bin/env python3

import serial

class arduinoSerialWrapper():
    '''
        
    '''
    def __init__(self, device, baudrate):
        self.arduino = serial.Serial(device, baudrate, timeout=1)

    def resetBuff(self):
        self.arduino.reset_input_buffer()
    
    def read(self):
        if self.arduino.in_waiting > 0:
            line = self.arduino.reaLine().decode('utf-8').rstrip()
        
        return line
    #TODO: to be continued

# if __name__ == "__main__":
#     arduino = serial.Serial(config.ardu_device, 9600, timeout=1)
#     arduino.reset_input_buffer()

#     while True:
#         if arduino.in_waiting > 0:
#             line = arduino.readline().decode('utf-8').rstrip()
#             print(line)