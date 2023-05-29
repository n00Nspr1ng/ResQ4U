from common import config
from common.imports import *

class Relay:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def toggle(self):
        if GPIO.input(self.pin):
            self.off()
        else:
            self.on()

if __name__ == '__main__':
    relay = Relay()
