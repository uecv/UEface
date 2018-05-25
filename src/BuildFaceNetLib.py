#coding:utf-8

'''
创建人脸特征库
'''


import json
import os
import cv2
from src.FaceFeature.FaceNet.FaceNetExtract import FaceNetExtract
from src.Config.Config import Config
from src.FaceDetection.MTCNNDetection import MTCNNDetection
import  numpy


class NPEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(NPEncoder, self).default(obj)


class buildLib:
    """
    what,how
    """
    def __init__(self,faceFeatureModel,faceDetect):


        self.faceFeatureModel = faceFeatureModel
        self.faceDetect = faceDetect

        self.imagesPath="./library/images/"

        self.libraryPath ="./library/faceNetLib/facerec_128D.txt"

    def build(self):

        data = open(self.libraryPath, 'r').read()
        data_set= {}
        if len(data)>0:

            data_set = json.loads(data)



        person_features = {"Left": [], "Right": [], "Center": []}

        images = os.listdir(self.imagesPath)

        for name_id in images:

            name, id = name_id.split("_")

            imagepath = os.path.join(self.imagesPath,name_id)

            im = cv2.imread(imagepath)

            # 人脸检测:
            # locations：人脸位置。  landmarks：人脸特征点
            locations, landmarks = faceDetect.detect(im)

            # ** 人脸特征抽取
            # features_arr：人脸特征    positions：人脸姿态
            features_arr, positions = faceFeature.Extract(im, locations, landmarks)



            for pos in person_features:
                person_features[pos] = features_arr

            data_set[id] = person_features


        f = open(self.libraryPath, 'w')
        f.write(json.dumps(data_set,cls=NPEncoder))

        f.close()




if __name__ == '__main__':

    conf = Config("./Config/config.ini")

    # ** 构建人脸特征库对象

    faceFeature = FaceNetExtract(conf)  # 人脸特征抽取接口

    faceDetect = MTCNNDetection(conf)  # 人脸 检测接口




    buildL = buildLib(faceFeature,faceDetect)

    buildL.build()
