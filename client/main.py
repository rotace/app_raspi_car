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

    if '/dev/ttyUSB0' in serial.tools.list_ports.comports()[0]:
        ser = serial.Serial('/dev/ttyUSB0', 9600)
    else:
        ser = None

    clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsock.connect((host, port))

    while True:
        time.sleep(0.1)
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
            if ser.inWaiting() > 0:
                print(ser.read(ser.inWaiting()))
            else:
                print("pass")

    if ser is None:
        print('close')
    else:
        ser.write(b'c')


if __name__ == '__main__':
    main()
