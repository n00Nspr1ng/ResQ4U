import time
from serial import Serial
import numpy as np


ser = Serial("/dev/ttyUSB0", 115200,timeout=0) # mini UART serial device



def get_TF_Data():
    while True:
        count = ser.in_waiting
        if count > 8:
            recv = ser.read(9)
            ser.reset_input_buffer()
            if recv[0] == 'Y' and recv[1] == 'Y': # 0x59 is 'Y'
                low = int(recv[2].encode('hex'), 16)
                high = int(recv[3].encode('hex'), 16)
                distance = low + high * 256
                print(distance)
                


if __name__ == '__main__':
    try:
        if ser.is_open == False:
            ser.open()
        print("serial open yes")
        get_TF_Data()
    except KeyboardInterrupt:   # Ctrl+C
        if ser != None:
            ser.close()
