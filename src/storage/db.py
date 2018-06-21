# coding=utf-8
"""
   @author: wy
   @time: 2018/6/18 0018
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine('mysql+pymysql://root:ueface@192.168.0.245:3306/ueface' , encoding="utf-8" , echo=True)
Base = declarative_base()
#engine = create_engine('mysql://root:ueface@192.168.0.10:3306/ueface' , encoding="utf-8" , echo=True)
Session = sessionmaker(bind=engine)
