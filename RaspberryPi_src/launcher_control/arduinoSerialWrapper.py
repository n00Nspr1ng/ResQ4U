#!/usr/bin/env python3

import serial
import time

class arduinoSerialWrapper():
    '''
    Wrapper for arduino serial communication.
    Args:
        device: The tty port number to connect.
                Usually set to /dev/ttyACM0.
        baudrate: Baudrate of arduino. Default is set to 9600.
    '''
    
    def __init__(self, device, baudrate=9600):

        # Open arduino communication
        try:
            self.arduino = serial.Serial(device, baudrate, timeout=1)
            time.sleep(1)
        except:
            print("Device can not be found or can not be configured.")

        self.reset_buff()


    def reset_buff(self):
        self.arduino.reset_input_buffer()


    def read(self):
        if self.arduino.in_waiting > 0:
            line = self.arduino.reaLine().decode('utf-8').rstrip()
        
        return line


    def send_speed(self, motor_speed):
        self.arduino.write(motor_speed)

        
    def check_done(self):
        while(True):
            if (self.arduino.readable()):
                done_flag = int(self.arduino.readline().decode('utf-8').rstrip())
                if (done_flag == True):
                    break
        return True


if __name__ == "__main__":
    arduino = arduinoSerialWrapper("/dev/ttyACM0", 9600, timeout=1)
    arduino.read()
    time.sleep(1)

    arduino.send_speed(100)
    arduino.check_done()

    