import cv2
import json
import numpy as np

import  sys


from src.FaceDetection.MTCNNDetection import    MTCNNDetection
from src.FaceFeature.FaceNet.FaceNetExtract import FaceNetExtract
'''
faceNet实现人脸识别的类：包括调用人脸特征检测，人脸特征抽取等
'''

class faceNetRecognition:

    def __init__(self):
        '''
        初始化人脸检测接口   人脸特征抽取接口
        '''

        self.DetectInterface =MTCNNDetection()

        self.FaceFeature = FaceNetExtract()


    def  face_locations_encoding(self,image):
        '''

        :param image:
        :param locations:  list类型，一系列人脸的位置
        :return: 输出人脸的位置，编码，姿态
        '''

        locations, landmarks =self.DetectInterface.detect(image)

        features_arr = []
        positions = []
        if len(locations)>0:
            features_arr, positions = self.FaceFeature.Extract(image, locations, landmarks)




        # rects (x,y,w,h) to (x1,y1,x2,y2)

        #locations  [ymin, xmin, ymax, xmax]
        for (i,l) in enumerate(locations):
            ymin = l[0]
            xmin = l[1]
            ymax = l[2]
            xmax = l[3]

            # cv2.rectangle(image, (xmin,ymax), (xmax,ymin), (255, 0, 0))





        return np.array(locations),features_arr,positions



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
    def findPeople(self,features_arr, positions, data_set=None,thres = 0.6, percent_thres = 85):
        '''
        :param features_arr: a list of 128d Features of all faces on screen
        :param positions: a list of face position types of all faces on screen
        :param thres: d
        istance threshold
        :return: person name and percentage
        '''
        if data_set is None:
            f = open('./facerec_128D.txt','r')
            data_set = json.loads(f.read())
        returnRes = [];
        for (i,features_128D) in enumerate(features_arr):
            result = "Unknown";
            smallest = sys.maxsize
            for person in data_set.keys():
                person_data = data_set[person][positions[i]];
                for data in person_data:
                    distance = np.sqrt(np.sum(np.square(data-features_128D)))
                    if(distance < smallest):
                        smallest = distance;
                        result = person;
            percentage =  min(100, 100 * thres / smallest)
            if percentage <= percent_thres :
                result = "Unknown"
            returnRes.append((result,percentage))
        return returnRes


    def Recognition(self,image,EncodingCache,known_face_dataset):

        face_locations, face_encodings, positions = self.face_locations_encoding(image)

        # 将人脸编码添加到缓存中
        for face in face_encodings:
            EncodingCache.append(face)

        face_names = []
        if len(face_locations) > 0:  # start(EncodingCache, face_encodings):  # 如果达到判断人脸的条件

            face_names = self.findPeople(face_encodings, positions, data_set=known_face_dataset)

        return face_names