import sys
sys.path.append('/home/roboin/ResQ4U/RaspberryPi_src/common')
from imports import *

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

        # Flags
        self.init_flag : bool = False
        self.detect_flag : bool = False
        self.align_flag : bool = False
        self.end_flag : bool = False

        # Flush buffer
        self.device.reset_input_buffer()
        
        while(self.init_flag == False):
            line = self.read_line()
            print(line)
            if (line() == "Arduino is ready"):
                self.init_flag = True


    def read_line(self):
        if self.device.readable():
            line = self.device.readline().decode('utf-8').rstrip()

            return line


    def check_end_flag(self): 
        if self.device.readable():
            line = self.device.readline().decode('utf-8').rstrip()
            print(line)

            if (line == "ended"):
                self.align_flag = False
                self.end_flag = True        


    def send_flag(self, flag):
        if (flag == "d"):
            self.detect_flag = True
        elif (flag == "a"):
            self.detect_flag = False
            self.align_flag = True

        self.device.write(flag.encode())


# if __name__ == "__main__":
#     device = SerialWrapper(arduino_uno)
#     device.read()
    
