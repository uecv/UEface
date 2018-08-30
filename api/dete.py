#!/usr/bin/env python 
# coding: utf-8 
""" 
   @author: kenwood
   @time: 18-8-21 下午3:45  
"""
import requests
from io import BytesIO
from PIL import Image
import os,base64
import cv2
import numpy as np
from src.FaceDetection.MTCNNDetection import MTCNNDetection
from settings import *

url = 'http://127.0.0.1:5000/face_detect'
image_root='/home/kenwood/图片'
image_path ='jianwu_1.jpg'
img = Image.open(os.path.join(image_root,image_path), 'r')
buffered = BytesIO()
img.save(buffered, format="JPEG")
raw_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
# print(raw_image)
# data= {'image':raw_image}
# content = requests.post(url,data=data)
# print (content)
frame = cv2.imdecode(np.frombuffer(base64.b64decode(raw_image), np.uint8), -1)
faceDetect = MTCNNDetection(mtcnnDeteModel)
locations, landmarks = faceDetect.detect(frame)
print (locations)