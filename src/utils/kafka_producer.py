#!/usr/bin/env python 
# coding: utf-8 
""" 
   @author: kenwood
   @time: 18-6-6 上午10:24  
"""
from pykafka import KafkaClient,Broker
import time
import json
import uuid
import random
import threading
import cv2
#创建kafka实例
hosts = '192.168.0.251:9092'
client = KafkaClient(hosts=hosts)

print(client.topics)

# 创建kafka producer句柄
topic = client.topics[b'frame']

src = "rtsp://admin:qwe123456@192.168.1.202:554/cam/realmonitor?channel=1&subtype=0"
video_capture = cv2.VideoCapture(src)

# work
def work():
    with topic.get_producer(max_queued_messages=500000,max_request_size=4000012) as producer:
        while True:
            video_capture.set(cv2.CAP_PROP_FPS,5)
            _, frame = video_capture.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # msg = json.dumps({
            #     "id": str(uuid.uuid4()).replace('-', ''),
            #     "type": random.randint(1, 5),
            #     "profit": random.randint(13, 100)}).encode('utf-8')
            producer.produce(frame.tobytes())
            time.sleep(60)

# 多线程执行
# thread_list = [threading.Thread(target=work) for i in range(10)]
# for thread in thread_list:
#     thread.setDaemon(True)
#     thread.start()
if __name__ == '__main__':
    work()


