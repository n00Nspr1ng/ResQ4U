import serial.tools.list_ports                        
import time
import numpy as np

ser = serial.Serial()
ser.port = '/dev/ttyUSB0'
ser.baudrate = 115200
                                                                                                                          
def getTFdata():
    while True :
        # print('in while')
        count = ser.in_waiting
        if count > 8:
            print('ser.read')
            recv = ser.read(9)

            ser.reset_input_buffer()

            if recv[0] == 0x59 and recv[1] == 0x59:
                distance = np.int16(recv[2] + np.int16(recv[3]<<8))
                strength = recv[4] + recv[5] * 256
                print("distance : ", distance)

            if recv[0] == 'Y' and recv[1] == 'Y':
                lowD = int(recv[2].encode('hex'), 16)
                highD = int(recv[3].encode('hex'), 16)
                distance = np.int16(lowD + np.int16(highD <<8))
                print("distance : ", distance)
            else :
                time.sleep(0.005)

if __name__ == '__main__':
    try :
        if ser.is_open == False:
            try:
                ser.open()
            except :
                print("open failed")
        getTFdata()
    except KeyboardInterrupt:
        if ser != None:
            ser.close()
