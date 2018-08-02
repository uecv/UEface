# coding:utf-8
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
import numpy as np
from src.utils import Constant

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
    def __init__(self,faceFeatureModel, faceDetect):
        self.faceFeatureModel = faceFeatureModel
        self.faceDetect = faceDetect
        self.imagesPath =  image_path #conf.get("lib","imagepath")
        # self.libraryPath = conf.get("lib","feature.file")

    def build(self):
        # isExists = os.path.exists(self.libraryPath)
        # data = []
        # if isExists:
        #     data = open(self.libraryPath, 'r').read()
        # data_set = {}
        # if len(data) > 0:
        #     data_set = json.loads(data)
        error=[]
        Companys = os.listdir(self.imagesPath)
        for company in Companys: # 遍历该目录下的所有公司
            if company =="lfw":
                continue
            companypath = self.imagesPath + "/" + company

            isdir = os.path.isdir(companypath)
            if not isdir:
                continue
            images = os.listdir(companypath)
            for name_id in images:
                imagepath = os.path.join(companypath,name_id)
                print(name_id)

                ss =  name_id.split(".")[0].split("-")
                if len(ss)!=2:
                    error.append(name_id)
                    continue
                name, worker_id = ss

                im = cv2.imdecode(np.fromfile(imagepath, dtype=np.uint8), -1)
                im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)


                # 人脸检测:
                # locations：人脸位置。  landmarks：人脸特征点
                locations, landmarks = faceDetect.detect(im)

                if len(locations) !=1:
                    '''如果在图片中检测到的人脸不止一个，或者为0个，则跳过该人脸'''
                    print("错误的照片{path}".format(path = imagepath))
                    continue

                people = perpleDB.People(name=name, image_path=name_id,company_id=company,worker_id=worker_id)

                dbasePeople = perpleDB.getfilterPeople(people)

                if len(dbasePeople)>0: #如果数据中，已经存在该用户的特征，则不需要再次进行特征抽取。（公司id，用户工号，名称）相等
                    continue

                perpleDB.insert_people(people)

                # ** 人脸特征抽取
                # features_arr：人脸特征    positions：人脸姿态
                features_arr, positions = faceFeature.Extract(im, locations, landmarks)
                # person_features = {"Left": [], "Right": [], "Center": []}
                # for pos in person_features:
                #     person_features[pos] = features_arr
                #
                # data_set[people.id] = person_features
                feature_str = base64.b64encode(features_arr.tostring()).decode("utf-8")

                featurebean = featureDB.Feature(people_id=people.id,feature=feature_str)
                featureDB.insert_feature(featurebean)
        print(error)

        # f = open(self.libraryPath, 'w')
        # f.write(json.dumps(data_set, cls=NPEncoder))
        # f.close()


if __name__ == '__main__':
    # ** 构建人脸特征库对象
    faceFeature = FaceNetExtract()  # 人脸特征抽取接口
    faceDetect = MTCNNDetection()  # 人脸 检测接口

    buildL = buildLib(faceFeature, faceDetect)
    buildL.build()
