#!/usr/bin/env python
# coding: utf-8
"""
   @author: kenwood
   @time: 18-5-17 下午12:47
"""
import cv2


class Camera():
    def __init__(self, src):
        self.video = cv2.VideoCapture(src)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        _, frame = self.video.read()
        return frame
