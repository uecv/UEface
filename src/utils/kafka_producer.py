#!/usr/bin/env python 
# coding: utf-8 
""" 
   @author: kenwood
   @time: 18-6-6 上午10:24  
"""
# from pykafka import KafkaClient,Broker
from kafka import KafkaProducer,SimpleProducer,SimpleClient
from kafka.errors import KafkaError
import numpy as np
import threading
import cv2
import time
import io

src = "rtsp://admin:qwe123456@192.168.1.202:554/cam/realmonitor?channel=1&subtype=0"
video_capture = cv2.VideoCapture(src)
#创建kafka实例
producer = KafkaProducer(bootstrap_servers='192.168.0.245:9092',max_request_size=4000000,api_version = (0, 10))



def video_emitter(video):
    # Open the video
    video = cv2.VideoCapture(video)
    print(' emitting.....')

    # read the file
    while (video.isOpened):
        # read the image in each frame
        success, image = video.read()
        # check if the file has read to the end
        if not success:
            break
        # convert the image png
        ret, jpeg = cv2.imencode('.png', image)
        # Convert the image to bytes and send to kafka
        producer.send('frame', jpeg.tobytes())
        # To reduce CPU usage create sleep time of 0.2sec
        time.sleep(0.2)
    # clear the capture
    video.release()
    print('done emitting')

if __name__ == '__main__':
    video_emitter(src)


# work
# 多线程执行
# thread_list = [threading.Thread(target=work) for i in range(10)]
# for thread in thread_list:
#     thread.setDaemon(True)



