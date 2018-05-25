#!/usr/bin/env python 
# coding: utf-8 
""" 
   @author: kenwood
   @time: 18-5-18 下午5:48  
"""
class BaseDetection():
    """
    人脸检测基类
    """
    def __init__(self,config):
        """
        加载配置
        :param config:
        """
        self.config = config


    def load(self):
        """
        加载模型
        :return:
        """
        pass


    def detect(self, image):
            '''
            人脸检测接口
            :param images:
            :return: 返回照片中人脸的位置 ,以及特征点
            '''
            pass

