"""
Main Program for server
"""
import sys
import threading

import pygame
import pygame.locals
from PyQt5 import QtCore, QtWidgets, QtNetwork

import video_receiver

class MainForm(QtWidgets.QMainWindow):
    """
    This is GUI main class.
    """
    def __init__(self):
        super(MainForm, self).__init__()
        cent_wid = QtWidgets.QWidget()
        cent_lay = QtWidgets.QVBoxLayout()
        cent_wid.setLayout(cent_lay)

        self.video_receiver = video_receiver.VideoReceiver()
        cent_lay.addWidget(self.video_receiver)

        self.gamepad_monitor = GamePadMonitor()
        cent_lay.addWidget(self.gamepad_monitor)

        self.drive_controller = DriveController()
        cent_lay.addWidget(self.drive_controller)

        self.gamepad_monitor.signalAccelL.connect(self.drive_controller.set_accel_l)
        self.gamepad_monitor.signalAccelR.connect(self.drive_controller.set_accel_r)

        self.setCentralWidget(cent_wid)
        self.setWindowTitle("app_raspi_car")
        self.resize(600,400)

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
        else:
            event.ignore()

class DriveController(QtWidgets.QGroupBox):
    """
    This is class for controlling driving.
    """    
    def __init__(self, parent=None):
        super(DriveController, self).__init__(parent=parent)

        def toggle_connect():
            if self.sock.state() == QtNetwork.QAbstractSocket.SocketState.ConnectedState:
                self.sock.disconnectFromHost()
            else:
                self.sock.connectToHost(cmb_addr.currentText(), int(cmb_port.currentText()))
        
        btn_connect = QtWidgets.QPushButton("Connect")
        cmb_addr = QtWidgets.QComboBox()
        cmb_port = QtWidgets.QComboBox()
        cmb_addr.addItems(["127.0.0.1", "raspberrypi.local"])
        cmb_port.addItems(["8090"])
        btn_connect.clicked.connect(toggle_connect)

        lay = QtWidgets.QFormLayout()
        lay.addRow("Connect TCP Server", btn_connect)
        lay.addRow("Connect Addr", cmb_addr)
        lay.addRow("Connect Port", cmb_port)
        self.setLayout(lay)
        self.setTitle(self.__class__.__name__)

        self.sock = QtNetwork.QTcpSocket()
        self.sock.readyRead.connect(self.tcp_ready_read)
        self.sock.stateChanged.connect(self.tcp_state_changed)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.send_command)

        self.btn_connect = btn_connect
        self.accel_l = 0
        self.accel_r = 0

    def tcp_ready_read(self):
        while self.sock.bytesAvailable():
            print(self.sock.readAll())

    def tcp_state_changed(self, state):
        if state == QtNetwork.QAbstractSocket.SocketState.ConnectedState:
            self.btn_connect.setText("Disconnect")
            self.timer.start(100)
        if state == QtNetwork.QAbstractSocket.SocketState.UnconnectedState:
            self.btn_connect.setText("Connect")
            self.timer.stop()

    def send_command(self):
        self.sock.write('a{0:4d}{1:4d}\n'.format(self.accel_l, self.accel_r).encode())
        print('data: {0} : {1}'.format(self.accel_l, self.accel_r))

    def set_accel_l(self, val):
        """ get accel left """
        self.accel_l = int(val/100*255)

    def set_accel_r(self, val):
        """ get accel right """
        self.accel_r = int(val/100*255)


class GamePadMonitor(QtWidgets.QGroupBox):
    """
    This is the class for monitoring gamepad.
    """
    signalAccelL = QtCore.pyqtSignal(float)
    signalAccelR = QtCore.pyqtSignal(float)

    def __init__(self, parent=None):
        super(GamePadMonitor, self).__init__(parent=parent)

        self.analog_l = QtWidgets.QProgressBar()
        self.analog_l.setMinimum(-100)
        self.analog_l.setMaximum(+100)
        self.analog_l.setValue(+20)
        self.signalAccelL.connect(self.analog_l.setValue)
        self.analog_r = QtWidgets.QProgressBar()
        self.analog_r.setMinimum(-100)
        self.analog_r.setMaximum(+100)
        self.analog_r.setValue(-20)
        self.signalAccelR.connect(self.analog_r.setValue)

        lay = QtWidgets.QFormLayout()
        lay.addRow("Left", self.analog_l)
        lay.addRow("Right", self.analog_r)
        self.setLayout(lay)
        self.setTitle(self.__class__.__name__)

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
