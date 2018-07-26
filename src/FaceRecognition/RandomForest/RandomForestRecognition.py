import json
import sys

import cv2
import numpy as np
import  pickle
from src.FaceRecognition.BaseRecognition import BaseRecognition

'''
faceNet实现人脸识别的类：包括调用人脸特征检测，人脸特征抽取等
'''


class RandomForestRecognition(BaseRecognition):

    def __init__(self,conf):
        '''
        初始化人脸检测接口   人脸特征抽取接口
        '''
        with open("LR.pickle", "rb") as fp:
            self.model = pickle.load(fp)






    def Recognit(self, known_face_dataset, face_encodings, positions):
        '''

        :param known_face_dataset:  人脸特征库

        :param face_encodings:  人脸特征，list对象，包含多个人脸特征
        :param positions:  人脸姿态：  正脸  左脸  右脸
        :return: 在人脸特征库中，匹配到的人脸ID
        '''

        face_ID =[]
        for face in face_encodings:

            maxAlpha = 0.0
            peopleid=""

            for temp in known_face_dataset:

                person_data = known_face_dataset[temp][positions[0]][0]

                x= (face - person_data)

                x = np.array(x).reshape(1, -1)

                result = self.model.predict(x*x)
                if result>maxAlpha:
                    maxAlpha = result
                    peopleid = temp
            # print((maxAlpha,peopleid))
            face_ID.append((peopleid,maxAlpha))







        return face_ID


