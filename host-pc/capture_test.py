#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2

URL = "http://192.168.2.104:9000/?action=stream&ignored.mjpg"
s_video = cv2.VideoCapture(URL)

while True:
  ret, img = s_video.read()
  cv2.imshow("Stream Video",img)
  key = cv2.waitKey(1) & 0xff
  if key == ord('q'): break
