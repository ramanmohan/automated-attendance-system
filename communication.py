'''@author: Raman import serial
import time
# configure the serial connections (the parameters differs on the device you are connecting to)

YELLOWON = b'RL11\r\n'
YELLOWOFF = b'RL10\r\n'
GREENON = b'RL21\r\n'
GREENOFF = b'RL20\r\n'

class serialCommunication:
    def __init__(self):
        self.ser = serial.Serial(port='/dev/ttyUSB0', baudrate=38400)
    
    def unknown(self):
        self.ser.write(YELLOWON)
        time.sleep(0.5)
        self.ser.write(YELLOWOFF)
    def detected(self):
        self.ser.write(GREENON)	
        time.sleep(0.5)
        self.ser.write(GREENOFF)
        
    def opem(self):
        self.ser.open()
        
    def clos(self):
        self.ser.close()

        
        
