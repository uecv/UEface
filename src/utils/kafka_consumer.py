#!/usr/bin/env python 
# coding: utf-8 
""" 
   @author: kenwood
   @time: 18-6-6 上午10:38  
"""
from kafka import KafkaConsumer
from PIL import Image
import io
import numpy as np
consumer = KafkaConsumer('frame',bootstrap_servers=['192.168.0.245:9092'],api_version = (0, 10))
for message in consumer:
    # print ("%s:%d:%d: key=%s value =%s" % (message.topic, message.partition,
    #                                       message.offset, message.key,message.value))
    # new_frame = (np.fromstring(message.value, dtype=np.uint8))
    # print (new_frame)
    image_data = message.value  # byte values of the image
    image = np.asarray(Image.open(io.BytesIO(image_data)))
    print(image)

