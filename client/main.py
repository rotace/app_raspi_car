"""
Main Program for client
"""
import configparser
import socket
import time

import serial
import serial.tools.list_ports


def main():
    " main function "

    inifile = configparser.ConfigParser()
    inifile.read('./config.ini', 'UTF-8')
    host = str(inifile.get('settings', 'host'))
    port = int(inifile.get('settings', 'port'))

    if '/dev/ttyUSB0' in list(serial.tools.list_ports.comports()):
        ser = serial.Serial('/dev/ttyUSB0', 9600)
    else:
        ser = None

    clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsock.connect((host, port))

    while True:
        time.sleep(0.01)
        try:
            clientsock.sendall(b'a')
            response = clientsock.recv(4096)
        except OSError:
            break

        if len(response) == 0:
            break

        if ser is None:
            print(response)
        else:
            ser.write(response)

    if ser is None:
        print('close')
    else:
        ser.write(b'close')


if __name__ == '__main__':
    main()
