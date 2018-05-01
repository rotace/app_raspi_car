"""
Main Program for client
"""
import configparser
import distutils.util
import socket
import time

import serial

def strtobool(obj):
    """
    This is function which convert string into bool.
    """
    return bool(distutils.util.strtobool(obj))

class Main():
    """
    This is Main Class.
    """
    def __init__(self):
        super().__init__()

        self.inifile = configparser.ConfigParser()
        self.inifile.read('./config.ini', 'UTF-8')
        self.server_address = str(self.inifile.get('settings', 'host'))
        self.server_port = int(self.inifile.get('settings', 'port'))
        self.has_controller = strtobool(self.inifile.get('flags', 'has_controller'))
        self.has_cammera = strtobool(self.inifile.get('flags', 'has_cammera'))
        self.has_arduino = strtobool(self.inifile.get('flags', 'has_arduino'))

        if self.has_arduino:
            self.ser = serial.Serial('/dev/ttyUSB0', 9600)
        else:
            self.ser = None

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server_address, self.server_port))

        self.send_command()

    def send_command(self):
        " send command "
        while True:
            time.sleep(0.01)
            response = self.client.recv(4096)
            if self.ser is not None:
                self.ser.write(response)

def main():
    " main function "
    Main()

if __name__ == '__main__':
    main()
