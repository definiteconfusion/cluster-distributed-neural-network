import serial

class Cluster:
    
    def __init__(self):
        # Port is specific to MacOS
        self.port = '/dev/cu.usbmodem1101'
        self.baudrate = 9600
        self.timeout = 100
        self.Serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)    
    
    def write(self, data):
        """
        Write data to the serial port.
        """
        self.Serial.write(data.encode())
        self.Serial.flush()
        
    def read(self):
        """
        Read data from the serial port.
        """
        data = self.Serial.readline()
        return data.decode().strip()
