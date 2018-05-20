#!/usr/bin/env python 
# coding: utf-8 
""" 
   @author: kenwood
   @time: 18-5-18 下午5:12  
"""
from src.FaceDetection.mtcnn_detection import MtcnnDetetion
from src.FaceRecognition import old_faceRecognition
from src.Config import Config
from src.utils import video_stream,Constant
#配置对象
config = Config()


#读取摄像头帧
frame = video_stream.Camera(config.get(Constant.VIDEO_SOURCE))
#检测人脸
detecter = MtcnnDetetion(config)
locations, landmarks = detecter.detect(frame)



#Todo 注释
(frame, face_names, now_time, image) = old_faceRecognition.recognition(
    frame, EncodingCache, known_face_dataset)