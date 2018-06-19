# coding=utf-8
import json
import sys
import  time
import cv2
import numpy as np
from src.FaceRecognition.BaseRecognition import BaseRecognition
from multiprocessing.dummy import Pool
# from multiprocessing import Pool
import  math
'''

faceNet实现人脸识别的类：包括调用人脸特征检测，人脸特征抽取等
'''


class faceNetRecognition(BaseRecognition):

    def __init__(self,conf):
        '''
        初始化人脸检测接口   人脸特征抽取接口
        '''

        self.pool  = Pool(8)


    def _cos(self,vector1, vector2):
        npvec1, npvec2 = np.array(vector1), np.array(vector2)
        return npvec1.dot(npvec2) / (math.sqrt((npvec1 ** 2).sum()) * math.sqrt((npvec2 ** 2).sum()))


    def Recognit(self, known_face_dataset, face_encodings, positions):
        '''

        :param known_face_dataset:  人脸特征库

        :param face_encodings:  人脸特征，list对象，包含多个人脸特征
        :param positions:  人脸姿态：  正脸  左脸  右脸
        :return: 在人脸特征库中，匹配到的人脸ID
        '''


        self.data_set = known_face_dataset

        face_ID = self.findPeople(
            face_encodings, positions, data_set=known_face_dataset)



        return face_ID


    # def face_locations_encoding(self, image):
    #     '''
    #
    #     :param image:
    #     :param locations:  list类型，一系列人脸的位置
    #     :return: 输出人脸的位置，编码，姿态
    #     '''
    #
    #     locations, landmarks = self.DetectInterface.detect(image)
    #
    #     features_arr = []
    #     positions = []
    #     if locations:
    #         features_arr, positions = self.FaceFeature.Extract(
    #             image, locations, landmarks)
    #
    #     # rects (x,y,w,h) to (x1,y1,x2,y2)
    #
    #     #locations  [ymin, xmin, ymax, xmax]
    #     for (i, l) in enumerate(locations):
    #         ymin = l[0]
    #         xmin = l[1]
    #         ymax = l[2]
    #         xmax = l[3]
    #
    #         cv2.rectangle(image, (xmin, ymax), (xmax, ymin), (255, 0, 0))
    #
    #     return np.array(locations), features_arr, positions, image


    def mapFunction(self,name):


        if name=="UEPEOPLE":
            return name,0,0.0

        # '61ce9a22-6e0d-11e8-a284-3ca06736b3e1'
        lib_person = self.data_set[name]['Center']

        if len(lib_person)<1:
            return name,0,0.0
        lib_person = lib_person[0]
        person = self.data_set['UEPEOPLE']
        t1 = time.time()
        simi = self._cos(lib_person, person)  # 相似度，越大越相似

        t2 = time.time()


        return  name,simi,t2-t1





    '''
    facerec_128D.txt Data Structure:
    {
    "Person ID": {
        "Center": [[128D vector]],
        "Left": [[128D vector]],
        "Right": [[128D Vector]]
        }
    }
    This function basically does a simple linear search for
    ^the 128D vector with the min distance to the 128D vector of the face on screen
    '''

    def findPeople(
            self,
            features_arr,
            positions,
            data_set=None,
            thres=0.6,
            percent_thres=0.75):
        '''
        :param features_arr: a list of 128d Features of all faces on screen
        :param positions: a list of face position types of all faces on screen
        :param thres: d
        istance threshold
        :return: person name and percentage
        '''
        if data_set is None:
            f = open('./facerec_128D.txt', 'r')
            data_set = json.loads(f.read())
        returnRes = []
        ######################################################

        '''使用map函数优化循环性能测试'''
        for people in features_arr:
            IDs_lib = list(self.data_set.keys())
            self.data_set['UEPEOPLE'] = people

            # 相似度列表，用户与人脸库中5000多个的相似度
            # import time
            # t1 = time.time()
            simi_result =  self.pool.map(self.mapFunction,IDs_lib)
            # t2 = time.time()
            # print("map操作时间：{t}".format(t = (t2 - t1)))

            simi_sort = sorted(simi_result,key= lambda x:x[1],reverse=True)
            # t3 = time.time()
            # print("排序操作时间：{t}".format(t=(t3 - t2)))

            # sumT = 0
            # for temp in simi_result:
            #     sumT = sumT + temp[2]
            #
            # maven = sumT / len(simi_result)

            # print("map操作的平均时间为：{t},一共有{cn}个数据，一共花费的时间{sumt}".format(t = maven,cn = len(simi_result),sumt = sumT))



            id,simi_max,_ = simi_sort[0]

            result = (id,simi_max)
            if simi_max < percent_thres:
                result = ('Unknown',0)
            returnRes.append(result)








        ######################################################
        # for (i, features_128D) in enumerate(features_arr):
        #     result = "Unknown"
        #     smallest =0.0 #sys.maxsize
        #     for person in data_set.keys():
        #         person_data = data_set[person][positions[i]]
        #         for data in person_data:
        #             # distance = np.sqrt(np.sum(np.square(data - features_128D)))
        #             distance =self._cos(data,features_128D)  # 相似度，越大越相似
        #             if distance > smallest:
        #                 smallest = distance
        #                 result = person
        #     # percentage = min(100, 100 * thres / smallest)
        #     if smallest <= percent_thres:
        #         result = "Unknown"
        #     returnRes.append((result, smallest))


        return returnRes
