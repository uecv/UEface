#!/usr/bin/env python 
# coding: utf-8 
""" 
   @author: kenwood
   @time: 18-5-30 上午9:56  
"""
import asyncio
import random

"""
任务型生产消费
"""
@asyncio.coroutine
def produce(queue,n):
    """
    生产者
    :param queue:
    :param n:
    :return:
    """
    for x in range(n):
        print ("producing{}/{}".format(x,n))
        yield from asyncio.sleep(random.random())
        item = str(x)
        yield from queue.put(item)

@asyncio.coroutine
def consume(queue):
    while True:
        item = yield from queue.get()
        print ('consumer ...{}'.format(item))
        yield from asyncio.sleep(random.random())
        queue.task_done()

@asyncio.coroutine
def run(n):
    queue = asyncio.Queue()
    #将coroutine 封装成 Task
    consumer = asyncio.ensure_future(consume(queue))
    yield from produce(queue,n)
    yield from queue.join()
    consumer.cancel()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(10))
    loop.close()
