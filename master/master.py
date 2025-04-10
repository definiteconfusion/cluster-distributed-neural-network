import serial
import time

class Cluster:
    
    def __init__(self):
        # Port is specific to MacOS
        self.port = '/dev/cu.usbmodem21101'  # Master Arduino
        self.baudrate = 19200
        self.timeout = 0.1
        try:
            self.Serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)    
            time.sleep(2)  # Give Arduino time to reset
            print(f"Successfully connected to {self.port}")
        except serial.SerialException as e:
            print(f"Error connecting to Arduino: {e}")
            raise
    
    def write(self, data):
        """
        Write data to the serial port.
        """
        print(f"Sending data: {data}")
        self.Serial.write(bytes(data, 'utf-8'))
        self.Serial.flush()
        
    def read(self):
        """
        Read data from the serial port.
        """
        data = self.Serial.readline()
        decoded = data.decode().strip()
        if decoded:
            print(f"\nReceived data: {decoded}\n")
        else:
            print("No data received")
        return decoded

    def read_all(self, timeout=5):
        """
        Read all available data with timeout.
        """
        responses = []
        start_time = time.time()
        while (time.time() - start_time) < timeout:
            if self.Serial.in_waiting > 0:
                data = self.read()
                if data:
                    responses.append(data)
            time.sleep(0.1)
        return responses


if __name__ == "__main__":
    # Test the Cluster class
    try:
        Test = Cluster()
        
        print("Sending command to master Arduino...")
        Test.write("1, 30, 0.5, 1.27, 2.3, 0.7, 0.5, 0.2\n")
        
        print("Waiting for responses...")
        responses = Test.read_all(timeout=5)
        
        print("Communication test results:")
        if responses:
            print(f"Received {len(responses)} response(s):")
            for i, response in enumerate(responses):
                print(f"  Response {i+1}: {response}")
        else:
            print("No responses received")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'Test' in locals() and hasattr(Test, 'Serial'):
            Test.Serial.close()
            print("Serial connection closed")