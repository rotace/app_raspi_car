"""
Main Program for server
"""
import configparser
import logging
import socket
import sys
import threading
from platform import python_version

import pygame
import pygame.locals
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import PYQT_VERSION_STR
from PyQt5.QtCore import QT_VERSION_STR
from sip import SIP_VERSION_STR

from gui import main_window_ui

# version check
print("## python ", python_version())
print("## Qt     ", QT_VERSION_STR)
print("## PyQt   ", PYQT_VERSION_STR)
print("## sip    ", SIP_VERSION_STR)
# assert(python_version() == '3.5.2')
# assert(QT_VERSION_STR == '5.6.2')
# assert(PYQT_VERSION_STR == '5.6')
# assert(SIP_VERSION_STR == '4.18')

logger = logging.getLogger('LoggingTest')
logger.setLevel(10)
fh = logging.FileHandler('main.log')
sh = logging.StreamHandler()
logger.addHandler(fh)
logger.addHandler(sh)

timer_interval = 20 # [milliseconds]


class MainForm(QtWidgets.QMainWindow, main_window_ui.Ui_MainWindow):
    """
    This is GUI main class.
    """
    def __init__(self):
        super(MainForm, self).__init__()
        self.setupUi(self)

        self.scene = QtWidgets.QGraphicsScene()
        self.pixitem = QtWidgets.QGraphicsPixmapItem()
        self.scene.addItem(self.pixitem)
        self.graphicsView.setScene(self.scene)

        self.analog_left_y.setValue(20)
        self.analog_right_y.setValue(-20)

        self.gamepad_monitor = GamePadMonitor()
        self.gamepad_monitor.signalAccelL.connect(self.analog_left_y.setValue)
        self.gamepad_monitor.signalAccelR.connect(self.analog_right_y.setValue)

        self.drive_controller = DriveController()
        self.gamepad_monitor.signalAccelL.connect(self.drive_controller.get_accel_l)
        self.gamepad_monitor.signalAccelR.connect(self.drive_controller.get_accel_r)

        self.actionClose.triggered.connect(self.closeEvent)
        self.statusbar.showMessage("Hello World")

    def closeEvent(self, event):
        """
        close Main Window (overwrited QMainWindow's Method)
        """
        ret = QtWidgets.QMessageBox.question(self, 'Message',
            'Are you sure to quit?', QtWidgets.QMessageBox.Yes |
            QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No )

        if ret == QtWidgets.QMessageBox.Yes:
            event.accept()
            self.gamepad_monitor.quit()
            # self.drive_controller.quit()
        else:
            event.ignore()

class DriveController(QtCore.QObject):
    """
    This is class for controlling driving.
    """    
    def __init__(self):
        super(DriveController, self).__init__()

        self.accel_l = 0
        self.accel_r = 0
        self.quit_flag = False

        inifile = configparser.ConfigParser()
        inifile.read('./config.ini', 'UTF-8')
        host = str(inifile.get('settings', 'host'))
        port = int(inifile.get('settings', 'port'))

        serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversock.bind((host, port))
        serversock.listen(10)

        thread = threading.Thread(target=self.worker_thread, args=(serversock, ))
        thread.daemon = True
        thread.start()

    def worker_thread(self, serversock):
        """ worker thread """
        while True:
            clientsock, (client_address, client_port) = serversock.accept()
            print('New client: {0} : {1}'.format(client_address, client_port))

            while True:
                try:
                    message = clientsock.recv(1024)
                    print('Recv: {0} from {1} : {2}'.format(message,
                                                            client_address,
                                                            client_port))
                except OSError:
                    break

                if len(message) == 0:
                    break

                clientsock.sendall('a{0:4d}{1:4d}\n'.format(self.accel_l, self.accel_r).encode())
                print('data: {0} : {1}'.format(self.accel_l, self.accel_r))

            clientsock.close()
            print('Connection Closed: {0} : {1}'.format(client_address, client_port))

    def get_accel_l(self, val):
        """ get accel left """
        self.accel_l = int(val/100*255)

    def get_accel_r(self, val):
        """ get accel right """
        self.accel_r = int(val/100*255)


class GamePadMonitor(QtCore.QObject):
    """
    This is the class for monitoring gamepad.
    """
    signalAccelL = QtCore.pyqtSignal(float)
    signalAccelR = QtCore.pyqtSignal(float)

    def __init__(self):
        super(GamePadMonitor, self).__init__()
        self.quit_flag = False
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self.start)
        self.thread.start()

    def start(self):
        """
        start
        """
        with self.lock:
            pygame.init()
            pygame.joystick.init()

            try:
                joys = pygame.joystick.Joystick(0)
                joys.init()
                print("connect joystick")
            except pygame.error:
                joys = None
                print("no joystick!")

            clock = pygame.time.Clock()
            while True:
                clock.tick(60)
                if joys is None:
                    pass
                else:
                    self.signalAccelL.emit(-100*joys.get_axis(1))
                    self.signalAccelR.emit(-100*joys.get_axis(3))
                for event in pygame.event.get():
                    if event.type == pygame.locals.QUIT:
                        pygame.quit()
                        break
                if self.quit_flag:
                    pygame.quit()
                    break

    def quit(self):
        """
        quit
        """
        self.quit_flag = True
        with self.lock:
            pass


def main():
    """
    Main Function
    """
    app = QtWidgets.QApplication(sys.argv)
    form = MainForm() # do not remove object "form" (avoid to delete MainForm)
    form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
