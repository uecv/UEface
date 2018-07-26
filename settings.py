#!/usr/bin/env python 
# coding: utf-8 
""" 
   @author: kenwood
   @time: 18-6-28 下午2:39  
"""
# coding = utf8
import os
from .src.Config import Config

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#[source]
source_path = ""

faceLibPath = './src/library/faceNetLib/facerec_128D.txt'
mtcnnDeteModel = './src/Model/faceNet/models/'
faceNetModel = "./src/Model/faceNet/models/model-20170512-110547.ckpt-250000"


feature_file="./src/library/faceNetLib/facerec_128D.txt"

#[cache]
image_path="./src/library/images"
redis_host="face_redis"
redis_port=7000

#[mysql]
mysql_host="face_mysql"
mysql_port=3306
mysql_user="root"
mysql_password="123456"
mysql_dbname="ueface"

#[web]
image_root="./src/library/images"
redis_queue="rq"
map_path ="./src/library/map"

#[log]
log_level = "debug"
log_dir = "./src//logs"