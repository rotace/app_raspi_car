import socket
import serial
import serial.tools.list_ports

HOST="127.0.0.1"
PORT=8090

def main():
    " main function "

    if '/dev/ttyUSB0' in serial.tools.list_ports.comports()[0]:
        ser = serial.Serial('/dev/ttyUSB0', 9600)
    else:
        ser = None

    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversock.settimeout(3)
    serversock.bind((HOST, PORT))
    serversock.listen(10)

    while True:
        try:
            clientsock, (client_address, client_port) = serversock.accept()
            print('New client: {0} : {1}'.format(client_address, client_port))
        except:
            print("timeout")
            continue

        while True:
            try:
                message = clientsock.recv(4096)
            except OSError:
                break

            if len(message) == 0:
                break

            if ser is None:
                print(message)
            else:
                ser.write(message)
                if ser.inWaiting() > 0:
                    print(ser.read(ser.inWaiting()))
                else:
                    print("pass")
        
        clientsock.close()
        print('Connection Closed: {0} : {1}'.format(client_address, client_port))

        if ser is None:
            print('close')
        else:
            ser.write(b'c')


if __name__ == '__main__':
    main()
