"""
Main Program for server
"""
import configparser
import logging
import socket
import sys
from platform import python_version

import pygame
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
        super().__init__()
        self.setupUi(self)

        self.show()

        self.scene = QtWidgets.QGraphicsScene()
        self.pixitem = QtWidgets.QGraphicsPixmapItem()
        self.scene.addItem(self.pixitem)
        self.graphicsView.setScene(self.scene)

        self.analog_left_y.setValue(20)
        self.analog_right_y.setValue(-20)

        self.gamepad_monitor = GamePadMonitor()
        self.gamepad_monitor.moveToThread(self.gamepad_monitor)
        self.gamepad_monitor.signalAccelL.connect(self.analog_left_y.setValue)
        self.gamepad_monitor.signalAccelR.connect(self.analog_right_y.setValue)
        self.gamepad_monitor.start()

        self.drive_controller = DriveController()
        self.drive_controller.moveToThread(self.drive_controller)
        self.gamepad_monitor.signalAccelL.connect(self.drive_controller.get_accel_l)
        self.gamepad_monitor.signalAccelR.connect(self.drive_controller.get_accel_r)
        self.drive_controller.start()

        self.actionClose.triggered.connect(self.closeEvent)
        self.actionConnectClient.triggered.connect(self.drive_controller.wait_connection)
        self.statusbar.showMessage("Hello World")

    def closeEvent(self, event):
        """
        close Main Window
        """
        confirmObject = QtWidgets.QMessageBox.question(self, 'Message',
            'Are you sure to quit?', QtWidgets.QMessageBox.Yes |
            QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No )

        if confirmObject == QtWidgets.QMessageBox.Yes:
            event.accept()
            self.gamepad_monitor.terminate()
        else:
            event.ignore()

class DriveController(QtCore.QThread):
    """
    This is class for controlling driving.
    """
    def __init__(self):
        super().__init__()
        self.mutex = QtCore.QMutex()

        self.accel_l = 0
        self.accel_r = 0

        self.inifile = configparser.ConfigParser()
        self.inifile.read('./config.ini', 'UTF-8')
        self.server_address = str(self.inifile.get('settings', 'host'))
        self.server_port = int(self.inifile.get('settings', 'port'))

        self.serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversock.bind((self.server_address, self.server_port))
        self.serversock.listen(10)

        self.client_address = None
        self.clientsock = None

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.send_command)
        self.timer.start(timer_interval)

    def wait_connection(self):
        """ wait connection """
        self.clientsock, self.client_address = self.serversock.accept()

    def send_command(self):
        """ send command """
        if self.clientsock is not None:
            self.clientsock.sendall('a{0:4d}{1:4d}\n'.format(self.accel_l, self.accel_r).encode())

    def get_accel_l(self, val):
        """ get accel left """
        self.accel_l = int(abs(val)/100*255)

    def get_accel_r(self, val):
        """ get accel right """
        self.accel_r = int(abs(val)/100*255)

class GamePadMonitor(QtCore.QThread):
    """
    This is the class for monitoring gamepad.
    """
    signalAccelL = QtCore.pyqtSignal(float)
    signalAccelR = QtCore.pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.mutex = QtCore.QMutex()

        pygame.init()
        pygame.joystick.init()

        try:
            self.joys = pygame.joystick.Joystick(0)
            self.joys.init()
            print("connect joystick")
        except pygame.error:
            self.joys = None
            print("no joystick!")

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.get_state)
        self.timer.start(timer_interval)

    def get_state(self):
        """ get state """
        if self.joys is not None:
            self.signalAccelL.emit(-100*self.joys.get_axis(1))
            self.signalAccelR.emit(-100*self.joys.get_axis(3))
            eventlist = pygame.event.get() # do not remove this line (magic sentence)
            # buttonlist = filter(lambda e : e.type == pygame.locals.JOYBUTTONDOWN , eventlist)
            # print( list(map(lambda x : x.button, buttonlist)) )

    def terminate(self):
        """ terminate """
        self.quit()
        pygame.quit()


def main():
    """
    Main Function
    """
    app = QtWidgets.QApplication(sys.argv)
    form = MainForm() # do not remove object "form" (avoid to delete MainForm)
    app.exec_()

if __name__ == '__main__':
    main()
