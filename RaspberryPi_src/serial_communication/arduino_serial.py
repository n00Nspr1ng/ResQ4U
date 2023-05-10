#!/usr/bin/env python3

import serial
import time

class SerialWrapper():
    '''
    Wrapper for serial communication.
    Args:
        device : dataclass from config.py that contains below.
                    - port : usually set to /dev/ttyACM0
                    - baudrate
    '''
    
    def __init__(self, device, timeout=1):

        # Open device communication
        try:
            self.device = serial.Serial(device.port, device.baudrate, timeout=1)
            time.sleep(1)
        except:
            print("Device can not be found or can not be configured.")

        # Flags to send to device
        self.detect_flag : int = 1
        self.align_flag : int = 2

        self.received : bool = False

        # Flush buffer
        self.device.reset_input_buffer()


    #Use either get_flag or wait_until_flag
    def get_flag(self): 
        if self.device.readable():
            line = self.device.readline().decode('utf-8').rstrip()
        
        return line

    def wait_until_done(self):
        while (True):
            if (self.device.readable()):
                break
     

    def send_flag(self, flag):
        self.device.write(flag.encode())


# if __name__ == "__main__":
#     device = SerialWrapper(arduino_uno)
#     device.read()
    