#!/usr/bin/env python 
# coding: utf-8 
""" 
   @author: kenwood
   @time: 18-6-6 上午10:38  
"""
from pykafka import KafkaClient

hosts = '192.168.0.251:9092'
client = KafkaClient(hosts=hosts)
# 消费者
topic = client.topics[b'frame']
consumer = topic.get_simple_consumer()
for message in consumer:
    if message is not None:
        print (message.offset, message.value)