#!/usr/bin/env python 
# coding: utf-8 
""" 
   @author: kenwood
   @time: 18-8-21 下午1:59  
"""
import tornado.httpserver
import tornado.web
import tornado.ioloop
import numpy as np
import cv2
import base64
from src.library.faceNetLib.faceNetFeatureLib import faceNetLib
from src.FaceDetection.MTCNNDetection import MTCNNDetection
from src.FaceFeature.FaceNet.FaceNetExtract import FaceNetExtract
from src.FaceRecognition.faceNet.faceNetRecognition import faceNetRecognition
from settings import *

facelib = faceNetLib()
# 人脸特征库
known_face_dataset = facelib.getlib()

# 人脸识别接口
Recognition = faceNetRecognition()
# 人脸 检测接口
faceDetect = MTCNNDetection(mtcnnDeteModel)
# 人脸特征抽取接口
faceFeature = FaceNetExtract(faceNetModel)

class facedecetehandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        #x-www-form-urlencoded
        image = self.get_argument('image')
        # print(image)
        frame = cv2.imdecode(np.frombuffer(base64.b64decode(image), np.uint8), -1)
        # print (frame)
        cv2.imread('/home/kenwood/图片/jianwu_1.jpg')
        locations, landmarks = faceDetect.detect(frame)
        print (locations)
        if locations:
            # ** 人脸特征抽取
            # features_arr：人脸特征    positions：人脸姿态
            features_arr, positions = faceFeature.Extract(
                frame, locations, landmarks)

            # ** 人脸识别/特征比对
            face_id = Recognition.Recognit(
                known_face_dataset, features_arr, positions)
            print (face_id)


