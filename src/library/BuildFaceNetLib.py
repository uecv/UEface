

'''
创建人脸特征库
'''


import json
import os

import cv2
import numpy as np
from src.Config.FaceNetconfig import config


class buildLib:
    def __init__(self):
        conf = config()

        self.faceFeatureModel = conf.getfaceFeatureModel()
        self.faceDetect = conf.getdetectionModel()
        self.alignerModel = conf.getalignerModel()

        self.faceNetLibPath = conf.getFaceNetLibPath()

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


buildL = buildLib()

buildL.build()
