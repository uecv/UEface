#!/usr/bin/env Python
# coding=utf-8
'''
创建人脸特征库
'''
import json
import  time
import os
import cv2
import numpy
from src.Config.Config import Config
from src.FaceDetection.MTCNNDetection import MTCNNDetection
from src.FaceFeature.FaceNet.FaceNetExtract import FaceNetExtract
from src.service import people as perpleDB
import numpy as np
from src.utils import Constant

from src.service.features import Feature,insert_feature


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
    def __init__(self, conf,faceFeatureModel, faceDetect):
        self.conf = conf
        self.faceFeatureModel = faceFeatureModel
        self.faceDetect = faceDetect
        self.imagesPath = conf.get("lib","imagepath")
        self.libraryPath = conf.get("lib","feature.file")

    def build(self):
        isExists = os.path.exists(self.libraryPath)
        data = []
        if isExists:
            data = open(self.libraryPath, 'r').read()
        data_set = {}
        if len(data) > 0:
            data_set = json.loads(data)
        Companys = os.listdir(self.imagesPath)
        for company in Companys: # 遍历该目录下的所有公司

            companypath = self.imagesPath + "/" + company  # os.path.join(self.imagesPath, name_id)
            # im = cv2.imread(imagepath)

            isdir = os.path.isdir(companypath)

            if not isdir:
                continue

            images = os.listdir(companypath)

            for name_id in images:

                imagepath = os.path.join(companypath,name_id)

                name, worker_id = name_id.split(".")[0].split("-")
                im = cv2.imdecode(np.fromfile(imagepath, dtype=np.uint8), -1)
                im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)


                # 人脸检测:
                # locations：人脸位置。  landmarks：人脸特征点
                locations, landmarks = faceDetect.detect(im)

                if len(locations) !=1:
                    '''如果在图片中检测到的人脸不止一个，或者为0个，则跳过该人脸'''
                    print("错误的照片{path}".format(path = imagepath))
                    continue


                # people = perpleDB.People(name=name, image_path=name_id,company_id=company,worker_id=worker_id)
                # print(people.id)
                # perpleDB.insert_people(people)

                # ** 人脸特征抽取
                # features_arr：人脸特征    positions：人脸姿态
                features_arr, positions = faceFeature.Extract(im, locations, landmarks)
                person_features = {"Left": [], "Right": [], "Center": []}
                for pos in person_features:
                    person_features[pos] = features_arr

                # data_set[people.id] = person_features

                str1 = features_arr.tostring()

                test = np.fromstring(str1,dtype=np.float32)

                featurebean = Feature(people_id=1,feature=features_arr.tostring())
                insert_feature(featurebean)


        f = open(self.libraryPath, 'w')
        f.write(json.dumps(data_set, cls=NPEncoder))
        f.close()


if __name__ == '__main__':
    conf = Config(Constant.CONFIG_PATH)
    # ** 构建人脸特征库对象
    faceFeature = FaceNetExtract(conf)  # 人脸特征抽取接口
    faceDetect = MTCNNDetection(conf)  # 人脸 检测接口

    buildL = buildLib(conf, faceFeature, faceDetect)
    buildL.build()
