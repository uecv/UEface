# coding=utf-8
"""
   @author: wy
   @time: 2018/6/18 0018
"""

import src.storage.db as db

# 必须引入相关的类,否则不会初始化建表
from src.service.people import  People

# 创建表
# from src.service.features import Feature


def intidb():
    db.Base.metadata.create_all(db.engine)

