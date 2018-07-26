# coding=utf-8
"""
   @author: wy
   @time: 2018/6/18 0018
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from settings import *


engine = create_engine('mysql+pymysql://{user}:{passwd}@{host}:{port}/{dbname}?charset=utf8'.format(\
    mysql_user=mysql_user,\
    passwd=mysql_password,\
    host=mysql_host,\
    port=mysql_port,\
    dbname=mysql_dbname), encoding="utf-8" , echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)