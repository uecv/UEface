
import  json
from settings import *
from src.service import  features as featuresDB

class  faceNetLib:
    def __init__(self,conf):
        pass
#         self._path = faceLibPath



    def getlib(self):
        known_face_dataset = featuresDB.getFeature()

#         f = open(self._path, 'r')
#         known_face_dataset = json.loads(f.read())  # 人脸特征库
#         f.close()

        return known_face_dataset
