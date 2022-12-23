import cv2
import numpy as np
from urllib import request
from PyQt5 import QtGui, QtCore, QtWidgets

class VideoReceiver(QtWidgets.QGroupBox):
    """
    This is class for receive videos.
    """    
    def __init__(self, parent=None):
        super(VideoReceiver, self).__init__(parent=parent)

        self.label = QtWidgets.QLabel("no video")

        lay = QtWidgets.QVBoxLayout()
        lay.addWidget(self.label)
        self.setLayout(lay)
        self.setTitle(self.__class__.__name__)

        self.stream=request.urlopen('http://raspberrypi.local:9000/?action=stream&ignored.mjpg')
        self.bytes=b''

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.disp_video)
        self.timer.start(1)

    def disp_video(self):
        self.bytes+=self.stream.read(1024)
        a = self.bytes.find(b'\xff\xd8')
        b = self.bytes.find(b'\xff\xd9')
        if a!=-1 and b!=-1:
            jpg = self.bytes[a:b+2]
            self.bytes= self.bytes[b+2:]
            img = QtGui.QImage()
            img.loadFromData(jpg, "JPG")
            pix = QtGui.QPixmap.fromImage(img)
            self.label.setPixmap(pix)


if __name__ == '__main__':
    stream=request.urlopen('http://raspberrypi.local:9000/?action=stream&ignored.mjpg')
    bytes=b''
    while True:
        bytes+=stream.read(1024)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a!=-1 and b!=-1:
            jpg = bytes[a:b+2]
            bytes= bytes[b+2:]
            i=cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
            cv2.imshow('i',i)
            if cv2.waitKey(1) ==27:
                exit(0)