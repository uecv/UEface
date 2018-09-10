# coding=utf-8
"""
   @author: wy
   @time: 2018/6/18 0018
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from settings import *
from src.utils import log
LOG = log.log()
"""
db_url = 'mysql+pymysql://{user}:{passwd}@{host}:{port}/{dbname}?charset=utf8'.format( \
    user=mysql_user, \
    mysql_user=mysql_user, \
    passwd=mysql_password, \
    host=mysql_host, \
    port=mysql_port, \
    dbname=mysql_dbname)
"""
db_url = 'mysql+pymysql://{user}@{host}:{port}/{dbname}?charset=utf8'.format( \
    user=mysql_user, \
    mysql_user=mysql_user, \
    host=mysql_host, \
    port=mysql_port, \
    dbname=mysql_dbname)


LOG.info(db_url)
engine = create_engine(db_url, encoding="utf-8" , echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)