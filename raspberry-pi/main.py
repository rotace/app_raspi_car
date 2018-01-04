
import time
import serial
import socket

class Main():
    def __init__(self):
        super(self.__class__, self).__init__()
        self.ser = serial.Serial('/dev/ttyUSB0', 9600)
        
        self.host = "192.168.0.7"
        self.port = 8080

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        
        self.send_command()

    def send_command(self):
        while(True):
            time.sleep(0.01)
            response = self.client.recv(4096)
            self.ser.write(response)

def main():
    Main()

if __name__ == '__main__':
    main()
