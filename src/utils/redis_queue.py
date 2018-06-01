#!/usr/bin/env python
# coding: utf-8
"""
   @author: kenwood
   @time: 18-5-17 上午11:51
"""

import redis

class RedisQueue(object):
    def __init__(self, name, host, port=6379,db=0):
        # redis的默认参数为：host='localhost', port=6379, db=0， 其中db为定义redis database的数量
        self.__db = redis.Redis(host=host, port=port, db=db)
        self.key = name

    def qsize(self):
        return self.__db.llen(self.key)  # 返回队列里面list内元素的数量

    def put(self, item):
        self.__db.rpush(self.key, item)  # 添加新元素到队列最右方

    def get_wait(self, timeout=None):
        # 返回队列第一个元素，如果为空则等待至有元素被加入队列（超时时间阈值为timeout，如果为None则一直等待）
        item = self.__db.blpop(self.key, timeout=timeout)
        # if item:
        #     item = item[1]  # 返回值为一个tuple
        return item

    def get_value(self,key):
        value = self.__db.get(key)
        return value


    def get_nowait(self):
        # 直接返回队列第一个元素，如果队列为空返回的是None
        item = self.__db.lpop(self.key)
        return item

    def set(self,key,value):
        self.__db.set(key,value)


if __name__ == '__main__':
    x = RedisQueue(name="sb",host='192.168.0.245', port=6379, db=0)