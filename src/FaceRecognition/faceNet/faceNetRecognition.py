import json
import sys

import cv2
import numpy as np
from src.FaceRecognition.BaseRecognition import BaseRecognition

'''
faceNet实现人脸识别的类：包括调用人脸特征检测，人脸特征抽取等
'''


class faceNetRecognition(BaseRecognition):

    def __init__(self,conf):
        '''
        初始化人脸检测接口   人脸特征抽取接口
        '''
        pass

    def _cos(self,vector1, vector2):
        dot_product = 0.0;
        normA = 0.0;
        normB = 0.0;
        for a, b in zip(vector1, vector2):
            dot_product += a * b
            normA += a ** 2
            normB += b ** 2
        if normA == 0.0 or normB == 0.0:
            return None
        else:
            return dot_product / ((normA * normB) ** 0.5)

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



        return face_ID[0]


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
            print("error")

        # '61ce9a22-6e0d-11e8-a284-3ca06736b3e1'
        lib_person = self.data_set[name]['Center']

        if len(lib_person)<1:
            return name,0
        lib_person = lib_person[0]
        person = self.data_set['UEPEOPLE']

        simi = self._cos(lib_person, person)  # 相似度，越大越相似

        return  name,simi





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
        from multiprocessing import Pool
        from multiprocessing.dummy import Pool as ThreadPool

        pool = ThreadPool()
        for people in features_arr:
            IDs_lib = list(self.data_set.keys())
            self.data_set['UEPEOPLE'] = people

            # 相似度列表，用户与人脸库中5000多个的相似度
            simi_result = pool.map(self.mapFunction,IDs_lib)
            simi_sort = sorted(simi_result,key= lambda x:x[1],reverse=True)

            id,simi_max = simi_sort[0]

            result = id
            if simi_max < percent_thres:
                result = 'Unknown'
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


        return returnRes,
