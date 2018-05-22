#!/usr/bin/env python 
# coding: utf-8 
""" 
   @author: kenwood，wy
   @time: 18-5-18 下午6:03  
"""
import  configparser

class Config:
    def __init__(self,path):
        ##Todo 读取配置见初始化元数据字典

        self._conf = configparser.RawConfigParser()
        self._conf.read(path)




    def set(self,key,value):
        self._conf[key]=value

    def get(self,root,key):
        return self._conf.get(root,key)

    ##Todo 参考开源库里面的实现，
    ## 取值为空的情况返回值
    ##　补全基础数据类型的get方法
    def getInt(self,key):
        return int(self._metaDict.get(key))