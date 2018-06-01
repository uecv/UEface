#!/usr/bin/env python
# coding: utf-8
"""
   @author: kenwood
   @time: 18-5-17 下午12:47
"""
import cv2
from src.Config.Config  import Config
import ConfigParser

cf = ConfigParser.ConfigParser()
cf.read("../Config/config.ini")

class Camera():
    def __init__(self,camid):
        """

        :param camid: string
        """
        kvs = dict(cf.items("camera"))
        self.src = kvs.get(camid)
        self.id = camid
        self.video = cv2.VideoCapture(self.src)
    def __del__(self):
        self.video.release()

    def get_frame(self):
        _, frame = self.video.read()
        return frame

    def get_camid(self):
        return self.id

