#!/usr/bin/env python 
# coding: utf-8 

class BaseRecognition():
    """
    人脸识别基类
    """
    def __init__(self,config):
        """
        加载配置
        :param config:
        """
        self.config = config

    def Recognit(self, known_face_dataset, face_encodings, positions):
        '''

        :param known_face_dataset:  人脸特征库

        :param face_encodings:  人脸特征，list对象，包含多个人脸特征
        :param positions:  人脸姿态：  正脸  左脸  右脸
        :return: 在人脸特征库中，匹配到的人脸ID
        '''
        pass