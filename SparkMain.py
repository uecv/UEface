# coding:utf-8

import base64
import datetime
import uuid
from io import BytesIO
import  numpy as np
import cv2
from PIL import Image
from src.Config import Config
from src.FaceDetection.MTCNNDetection import MTCNNDetection
from src.FaceFeature.FaceNet.FaceNetExtract import FaceNetExtract
from src.FaceRecognition.faceNet.faceNetRecognition import faceNetRecognition
from src.library.faceNetLib.faceNetFeatureLib import faceNetLib
from src.utils.redis_queue import RedisQueue
from src.utils import Constant,log
from src.DrawPicture.DrawFace import ImageUtil
from pyspark import  SparkContext




def map_function(id):

    LOG = log.log()
    LOG.debug('this is a test')
    redis_connect = RedisQueue(
        host='192.168.0.245',
        port=6379)

    src = "rtsp://admin:qwe123456@192.168.1.202:554/cam/realmonitor?channel=1&subtype=0"
    video_capture = cv2.VideoCapture(0)
    # video_capture.set(cv2.CAP_PROP_POS_FRAMES,25)
    conf = Config.Config(Constant.CONFIG_PATH)

    # 构建人脸特征库对象
    facelib = faceNetLib(conf)
    # 人脸特征库
    known_face_dataset = facelib.getlib()

    # 人脸识别接口
    Recognition = faceNetRecognition(conf)
    # 人脸 检测接口
    faceDetect = MTCNNDetection(conf)
    # 人脸特征抽取接口
    faceFeature = FaceNetExtract(conf)



    def map_detect(frame):
        # 人脸检测:
            # locations：人脸位置。  landmarks：人脸特征点
        locations, landmarks = faceDetect.detect(frame)



        return locations,landmarks


    while True:
        '''获取一帧视频'''
        ret,frame = video_capture.read()
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        locations, landmarks = map_detect(frame)
        features_arr, positions = faceFeature.Extract(
            frame, locations, landmarks)
        # ** 人脸识别/特征比对
        face_id = Recognition.Recognit(
            known_face_dataset, features_arr, positions)
        print("success")
        print(face_id)




sc = SparkContext("local")
sc.parallelize(range(2)).map(map_function).collect()





