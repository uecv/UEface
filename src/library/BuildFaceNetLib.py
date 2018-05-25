#coding:utf-8

'''
创建人脸特征库
'''


import json
import os
import cv2
import numpy as np
from src.Config.FaceNetFactory import FaceDetectionFactory
from src.FaceFeature.FaceNet.FaceNetExtract import FaceNetExtract
from src.Config.Config import Config
from src.FaceDetection.MTCNNDetection import MTCNNDetection


class buildLib:
    """
    what,how
    """
    def __init__(self):
        conf = FaceDetectionFactory()

        self.faceFeatureModel = conf.getfaceFeatureModel()
        self.faceDetect = conf.getdetectionModel()
        self.alignerModel = conf.getalignerModel()


        self.imagesPath = conf.getImagePath()

    def build(self):

        f = open(self.faceNetLibPath, 'r')
        data_set = json.loads(f.read())

        person_imgs = {"Left": [], "Right": [], "Center": []}
        person_features = {"Left": [], "Right": [], "Center": []}

        images = os.listdir(self.imagesPath)

        for name_id in images:

            name, id = name_id.split("_")
            print("success")

        im = cv2.imread("jianwu1.jpg")
        rects, landmarks = self.faceDetect.detect_face(
            im, 80)  # min face size is set to 80x80

        for (i, rect) in enumerate(rects):
            aligned_frame, pos = self.alignerModel.align(160, im, landmarks[i])
            if len(aligned_frame) == 160 and len(aligned_frame[0]) == 160:
                person_imgs[pos].append(aligned_frame)

        Feature = []
        for pos in person_features:  # there r some exceptions here, but I'll just leave it as this to keep it simple

            feature = [
                np.mean(
                    self.faceFeatureModel.get_features(
                        person_imgs[pos]),
                    axis=0).tolist()]
            nannum = np.isnan(feature).sum()
            if nannum == 0:
                Feature = feature

        for pos in person_features:
            person_features[pos] = Feature

        data_set["jianwu"] = person_features
        f = open('./facerec_128D.txt', 'w')
        f.write(json.dumps(data_set))


if __name__ == '__main__':

    conf = Config("./Config/config.ini")

    # ** 构建人脸特征库对象

    faceFeature = FaceNetExtract(conf)  # 人脸特征抽取接口

    faceDetect = MTCNNDetection(conf)  # 人脸 检测接口
    



    buildL = buildLib()

    buildL.build()
