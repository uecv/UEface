#coding:utf-8

'''
创建人脸特征库
'''
import json
import os
import cv2
import numpy
from src.Config.Config import Config
from src.FaceDetection.MTCNNDetection import MTCNNDetection
from src.FaceFeature.FaceNet.FaceNetExtract import FaceNetExtract
from src.service import people as perpleDB

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
        self.libraryPath = conf.get("lib","featurefile")

    def build(self):
        data = open(self.libraryPath, 'r').read()
        data_set = {}
        if len(data) > 0:
            data_set = json.loads(data)
        images = os.listdir(self.imagesPath)
        for name_id in images:
            name, id = name_id.split("_")
            imagepath = os.path.join(self.imagesPath, name_id)
            im = cv2.imread(imagepath)





            people = perpleDB.People(name,im )
            perpleDB.insert_people(people)


            # 人脸检测:
            # locations：人脸位置。  landmarks：人脸特征点
            locations, landmarks = faceDetect.detect(im)

            # cv2.imshow("test", im)
            # cv2.waitKey(0)

            location = locations[0]
            ymax = location[0]

            xmin = location[1]

            ymin = location[2]

            xmax = location[3]

            head = im[xmin:xmax, ymin:ymax, 0:3]


            cv2.imshow("jj",head)
            cv2.waitKey(0)


            # ** 人脸特征抽取
            # features_arr：人脸特征    positions：人脸姿态
            features_arr, positions = faceFeature.Extract(im, locations, landmarks)

            person_features = {"Left": [], "Right": [], "Center": []}

            for pos in person_features:
                person_features[pos] = features_arr

            data_set[people.id] = person_features


        f = open(self.libraryPath, 'w')
        f.write(json.dumps(data_set, cls=NPEncoder))
        f.close()




if __name__ == '__main__':
    conf = Config("./Config/config.ini")
    # ** 构建人脸特征库对象

    faceFeature = FaceNetExtract(conf)  # 人脸特征抽取接口

    faceDetect = MTCNNDetection(conf)  # 人脸 检测接口




    buildL = buildLib(faceFeature,faceDetect)

    buildL.build()
