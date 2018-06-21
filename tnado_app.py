#!/usr/bin/env python
# coding: utf-8
"""
   @author: kenwood
   @time: 18-5-29 上午9:34
"""
import tornado.ioloop
from tornado.ioloop import IOLoop
import tornado.web
import tornado.httpserver
import tornado.websocket
from PIL import Image
from io import BytesIO
from src.service import people
import base64
import time
from src.utils import Constant
from src.utils.redis_queue import RedisQueue
import json
from src.Config import Config
import os
conf = Config.Config(Constant.CONFIG_PATH)
redis_host = conf.get('web', 'redis_host')
redis_port = conf.get('web', 'redis_port')
redis_queue = conf.get('web', 'redis_queue')
image_root = conf.get('web', 'image_root')
map_path = conf.get('web', 'map_path')

queue = RedisQueue(
    host='192.168.0.245',
    port=6379)
count = 0
class SocketHandler(tornado.websocket.WebSocketHandler):
    def simple_init(self):
        self.last = time.time()
        self.stop = False

    def open(self):
        self.simple_init()
        print("New client connected")
        self.write_message("You are connected")
        #定时调度器
        self.loop = tornado.ioloop.PeriodicCallback(
            self.check_ten_seconds, 1000)
            #io_loop=tornado.ioloop.IOLoop.instance())
        self.loop.start()

    def on_message(self, message):
        print ('message',message)
        self.write_message(message)
        self.last = time.time()

    def on_close(self):
        print("Client disconnected")
        self.loop.stop()

    def check_origin(self, origin):
        return True

    def check_ten_seconds(self):
        print("Just checking")
        global  count
        #recognition result
        data = queue.get_nowait(redis_queue).decode('utf-8')
        count +=1
        # people_num
        msg = dict({
            "type": "GET_COUNT",
            "NUMS": count
        })
        # print(eval(data)['user_id'])

        result = eval(data)
        name,image_path = people.get_people(eval(data)['user_id'])

        #人脸库照片
        img = Image.open(os.path.join(image_root,image_path), 'r')
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        raw_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

        result_dict = dict({'ts': result['ts'],
                       #Todo 读数据库
                       'name': name,
                       'image': result['head_image'],
                       'id':   result['id'],
                       'raw_image': raw_image,
                       'similarity': result['similarity'],
                       'type': "GET_RECO_RESULT"})
        if (time.time() - self.last > 1):
            self.write_message(msg)
            self.write_message(result_dict)
            self.last = time.time()


class CamHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

        img = Image.open('/home/kenwood/cat.jpeg', 'r')
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        cam_dict = {
            "map": img_str,
            "camera": [{
                "name": "摄像头A",
                "id": 1,
                "url": "http://192.168.0.245/livestream.flv",
                # "url":"http://live.useease.cn/live/livestream.flv?auth_key=1528096827-0-0-7a54cf956bee59637d10309a96b2969a",
                "x": 30,
                "y": 50
            },
                {
                    "name": "摄像头B",
                    "id": 2,
                    "url": "http://192.168.0.245/livestream.flv",
                    # "url": "http://live.useease.cn/live/livestream.flv?auth_key=1528096827-0-0-7a54cf956bee59637d10309a96b2969a",
                    "x": 70,
                    "y": 80,
            }]
        }
        self.write(cam_dict)
def make_app():
    return tornado.web.Application([
        (r"/get_camera", CamHandler),
        (r'/live', SocketHandler),
    ])

def main():
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(5000)
    server.start(0)  # forks one process per cpu
    IOLoop.current().start()

if __name__ == '__main__':
    main()
