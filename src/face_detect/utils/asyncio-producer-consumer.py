#!/usr/bin/env python 
# coding: utf-8 
""" 
   @author: kenwood
   @time: 18-5-30 上午10:57  
"""
import asyncio
import random

"""
一直生产消费
"""
@asyncio.coroutine
def produce(queue,n):
    for x in range(1,n+1):
        print ('producing{}/{}'.format(x,n))
        yield from asyncio.sleep(random.random())
        item = str(x)
        yield from queue.put(item)


@asyncio.coroutine
def consume(queue):
    while True:
        item = yield from queue.get()
        if item is None:
            break
        print ('consuming item {}..'.format(item))
        yield from asyncio.sleep(random.random())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue()
    produce_coro = produce(queue,10)
    consumer_coro = consume(queue)
    loop.run_until_complete(asyncio.gather(produce_coro,consumer_coro))
    loop.close()


