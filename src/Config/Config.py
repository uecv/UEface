#!/usr/bin/env python 
# coding: utf-8 
""" 
   @author: kenwood，wy
   @time: 18-5-18 下午6:03  
"""
class Config:
    def __init__(self,path):
        ##Todo 读取配置见初始化元数据字典
        self._metaDict={}
        pass

    def set(self,key,value):
        self._metaDict[key]=value

    def get(self,key):
        return self._metaDict.get(key,None)

    ##Todo 参考开源库里面的实现，
    ## 取值为空的情况返回值
    ##　补全基础数据类型的get方法
    def getInt(self,key):
        return int(self._metaDict.get(key))