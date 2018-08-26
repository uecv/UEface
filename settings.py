#!/usr/bin/env python 
# coding: utf-8 
""" 
   @author: kenwood
   @time: 18-6-28 下午2:39  
"""
# coding = utf8
import os
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#[source]
source_path = "/UEface/test.mp4"

faceLibPath = os.path.join(BASE_DIR,"src/library/faceNetLib/facerec_128D.txt")
mtcnnDeteModel = os.path.join(BASE_DIR,"src/Model/faceNet/models/")
faceNetModel = os.path.join(BASE_DIR,"src/Model/faceNet/models/model-20170512-110547.ckpt-250000")


feature_file=os.path.join(BASE_DIR,"src/library/faceNetLib/facerec_128D.txt")

#[cache]
image_path=os.path.join(BASE_DIR,"src/library/images")
redis_host="face_redis"
redis_port=6379

#[mysql]
mysql_host="face_mysql"
mysql_port=3306
mysql_user="root"
mysql_password="123456"
mysql_dbname="ueface"

#[web]
image_root=os.path.join(BASE_DIR,"src/library/images")
redis_queue="rq"
map_path =os.path.join(BASE_DIR,"src/library/map")

#[log]
log_level = "debug"
log_dir = os.path.join(BASE_DIR,"logs")