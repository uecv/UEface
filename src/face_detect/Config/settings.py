#!/usr/bin/env python 
# coding: utf-8 
""" 
   @author: kenwood
   @time: 18-6-28 下午2:39  
"""
# coding = utf8
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

faceLibPath = './src/library/faceNetLib/facerec_128D.txt'
mtcnnDeteModel = './src/Model/faceNet/models/'
faceNetModel = "./src/Model/faceNet/models/model-20170512-110547.ckpt-250000"


imagepath="./src/library/images"
feature_file="./src/library/faceNetLib/facerec_128D.txt"

#[cache]
image_path="./src/library/images"
redis_host="192.168.0.245"
redis_prot=6379

#[mysql]
host="192.168.0.245"
port=3306
user="root"
password="123456"
#[web]
image_root="./src/library/images"
redis_queue="rq"
map_path ="./src/library/map"

#[log]
log_level = "debug"
log_dir = "./src//logs"