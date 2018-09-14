#!/usr/bin/env python 
# coding: utf-8 
""" 
   @author: kenwood
   @time: 18-6-28 下午2:39  
"""
# coding = utf8
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#[source]
source_path = "/build/testVideo.mp4"


#[model]
mtcnnDeteModel = os.path.join(BASE_DIR,"src/Model/faceNet/models/")
faceNetModel = os.path.join(BASE_DIR,"src/Model/faceNet/models/model-20170512-110547.ckpt-250000")


#[cache]
image_path=os.path.join(BASE_DIR,"src/library/images")
redis_host="localhost"
redis_port=6379

#[mysql]
mysql_host="localhost"
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