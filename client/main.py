"""
Main Program for client
"""
import configparser
import distutils.util
import socket
import time

import serial

class Main():
    """
    This is Main Class.
    """
    def __init__(self):
        super().__init__()

        inifile = configparser.ConfigParser()
        inifile.read('./config.ini', 'UTF-8')
        host = str(inifile.get('settings', 'host'))
        port = int(inifile.get('settings', 'port'))
        has_arduino = bool(distutils.util.strtobool(inifile.get('flags', 'has_arduino')))

        if has_arduino:
            self.ser = serial.Serial('/dev/ttyUSB0', 9600)
        else:
            self.ser = None

        self.clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsock.connect((host, port))

        self.send_command()

    def send_command(self):
        " send command "
        while True:
            time.sleep(1)
            self.clientsock.sendall(b'a')
            response = self.clientsock.recv(4096)
            if self.ser is None:
                print(response)
            else:
                self.ser.write(response)

def main():
    " main function "
    Main()

if __name__ == '__main__':
    main()
