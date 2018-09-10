#!/usr/bin/env python 
# coding: utf-8 
""" 
   @author: kenwood
   @time: 18-5-30 下午2:08  
"""
import multiprocessing
import asyncio
import time

class Consumer(multiprocessing.Process):
    def __init__(self,task_queue,result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                print ("{} is exiting".format(proc_name))
                self.task_queue.task_done()
                break
            print("%s:%s"%(proc_name,next_task))
            answer = next_task
            self.task_queue.task_done()
            self.result_queue.put(answer)
        return

class Task():
    def __init__(self,a,b):
        self.a = a
        self.b = b
    def __call__(self):
        time.sleep(0.1)
        return '%s * %s = %s'%(self.a,self.b,self.a *self.b)

    def __str__(self):
        return '%s * %s'%(self.a,self.b)

if __name__ == '__main__':
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    num_consumers = multiprocessing.cpu_count()*2
    print ('creating %d consumers'%num_consumers)
    consumers = [Consumer(tasks,results)for i in range(num_consumers)]
    start = time.time()
    for w in consumers:
        w.start()

    num_jobs = 10

    for i in range(num_jobs):
        tasks.put(Task(i,i))

    # Add a poison pill for each consumer
    for i in range(num_consumers):
        tasks.put(None)

    # Wait for all of the tasks to finish
    tasks.join()
    end = time.time()

    # Start printing results
    while num_jobs:
        result = results.get()
        print('Result:', result)
        num_jobs -= 1

    print("Running for %.3fs" % (end - start))






