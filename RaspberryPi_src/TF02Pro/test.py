from serial import Serial
import serial
import numpy as np

# data type setting (header & uart)
HEADER = 0x59
uart = [0] * 9


# ser = Serial("/dev/ttyAMA0", 115200,timeout=0) # mini UART serial device

# serial setting
ser = Serial(
    port = "/dev/ttyAMA0",
    baudrate = 115200,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 3
)

# or change it to :::::: while True
while(1) : 
    if ser.in_waiting > 0 :
        print("serial wating > 0")
        
        if ser.readline() == HEADER :
            
            print("read on") #for checking
            print(HEADER)
            uart[0] = HEADER
            
            if ser.readline() == HEADER :
                uart[1] = HEADER
                
                for i in range(2, 9):
                    uart[i] = int.from_bytes(ser.readline(), byteorder = 'little')
                check = uart[0]+uart[1]+uart[2]+uart[3]+uart[4]+uart[5]+uart[6]+uart[7]

                if uart[8] == (check & 0xff):
                    dist = uart[2] + uart[3] *256
                    strength = uart[4] + uart[5] *256
                    print("distance =", dist)
                    print("strength = ", strength)
