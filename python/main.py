
import sys
import os
import time
import logging
import serial

import pygame
from pygame.locals import *

from PyQt5 import QtGui, QtWidgets, QtCore


# version check
from platform import python_version
from PyQt5.QtCore import QT_VERSION_STR
from PyQt5.Qt import PYQT_VERSION_STR
from sip import SIP_VERSION_STR
print("## python ",python_version())
print("## Qt     ",QT_VERSION_STR)
print("## PyQt   ",PYQT_VERSION_STR)
print("## sip    ",SIP_VERSION_STR)
# assert(python_version() == '3.5.2')
# assert(QT_VERSION_STR == '5.6.2')
# assert(PYQT_VERSION_STR == '5.6')
# assert(SIP_VERSION_STR == '4.18')

from gui import main_window

logger = logging.getLogger('LoggingTest')
logger.setLevel(10)
fh = logging.FileHandler('main.log')
sh = logging.StreamHandler()
logger.addHandler(fh)
logger.addHandler(sh)

timer_interval=20 # [milliseconds]

class MainForm(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.show()

        self.scene = QtWidgets.QGraphicsScene()
        self.pixitem = QtWidgets.QGraphicsPixmapItem()
        self.scene.addItem(self.pixitem)
        self.graphicsView.setScene(self.scene)

        self.analog_left_x.setValue(20)
        self.analog_right_y.setValue(-20)

        self.gamepad_monitor = GamePadMonitor()
        self.gamepad_monitor.moveToThread(self.gamepad_monitor)
        self.gamepad_monitor.signalAccel.connect(self.analog_left_x.setValue)
        self.gamepad_monitor.signalSteer.connect(self.analog_right_y.setValue)
        self.gamepad_monitor.start()
        
        self.drive_controller = DriveController()
        self.drive_controller.moveToThread(self.drive_controller)
        self.gamepad_monitor.signalAccel.connect(self.drive_controller.get_accel)
        self.gamepad_monitor.signalSteer.connect(self.drive_controller.get_steer)
        self.drive_controller.start()

    def closeEvent(self, event):
        confirmObject = QtWidgets.QMessageBox.question(self, 'Message',
        'Are you sure to quit?', QtWidgets.QMessageBox.Yes |
        QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No )

        if confirmObject == QtWidgets.QMessageBox.Yes:
            event.accept()
            self.gamepad_monitor.terminate()
        else:
            event.ignore()

class DriveController(QtCore.QThread):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.mutex = QtCore.QMutex()
        self.ser = serial.Serial('/dev/ttyUSB0', 9600)
        
        self.accel = 0
        self.steer = 0

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.send_command)
        self.timer.start(timer_interval)

    def send_command(self):
        self.ser.write(bytes('a{0:4d}{1:4d}\n'.format(self.steer, self.accel), 'UTF-8'))
        # logger.info('a{0:4d}{1:4d}\n'.format(self.steer, self.accel))
        
    def get_accel(self, val):
        self.accel = int(abs(val)/100*255)
        
    def get_steer(self, val):
        self.steer = int(abs(val)/100*255)

class GamePadMonitor(QtCore.QThread):
    signalAccel = QtCore.pyqtSignal( float )
    signalSteer = QtCore.pyqtSignal( float )

    def __init__(self):
        super(self.__class__, self).__init__()
        self.mutex = QtCore.QMutex()

        pygame.init()
        pygame.joystick.init()

        try:
            self.joys = pygame.joystick.Joystick(0)
            self.joys.init()
        except pygame.error:
            print( 'no joystick!' )

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.get_state)
        self.timer.start(timer_interval)

    def get_state(self):
        self.signalAccel.emit( +100*self.joys.get_axis(0) )
        self.signalSteer.emit( -100*self.joys.get_axis(3) )

        eventlist = pygame.event.get()
        # buttonlist = filter(lambda e : e.type == pygame.locals.JOYBUTTONDOWN , eventlist)
        # print( list(map(lambda x : x.button, buttonlist)) )

    def terminate(self):
        self.quit()
        pygame.quit()


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = MainForm()
    app.exec_()

if __name__ == '__main__':
    main()
