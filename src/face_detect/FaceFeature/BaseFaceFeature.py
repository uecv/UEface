#!/usr/bin/env python 
# coding: utf-8 

class BaseFaceFeature():
    """
    人脸特征抽取基类
    """
    def __init__(self,config):
        """
        加载配置
        :param config:
        """
        self.config = config

    def Extract(self, image, locations, landmarks):
        '''
        输入人脸的坐标位置以及人脸特征点向量
        :param rects:  人脸坐标位置  shape = [N,4]  [ymin, xmin, ymax, xmax]
         :param landmarks:  特征点向量
         :param image : 原始照片
        :return:
        '''
        pass