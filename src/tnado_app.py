#!/usr/bin/env python
# coding: utf-8
"""
   @author: kenwood
   @time: 18-5-29 上午9:34
"""
import base64
import time
from io import BytesIO

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
from PIL import Image
from tornado.ioloop import IOLoop

from settings import *
from src.service import people
from src.utils.redis_queue import RedisQueue
from src.service import recoginiton


queue = RedisQueue(
    host=redis_host,
    port=redis_port)
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
        #print("Just checking")
        global  count
        #recognition result

        if queue.qsize('rq') == 0:
            #print("rq size 0")
            return

        data = queue.get_nowait(redis_queue).decode('utf-8')
        count +=1
        # people_num
        msg = dict({
            "type": "GET_COUNT",
            "NUMS": count
        })
        # print(eval(data)['user_id'])

        result = eval(data)
        print(result)
        info = people.get_people(result['user_id'])

        #人脸库照片

        company_path = os.path.join(image_root,info.company_id)
        #print(os.path.join(company_path,info.image_path))
        img = Image.open(os.path.join(company_path,info.image_path), 'r')

        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        raw_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

        result_dict = dict({'ts': result['ts'],
                       #Todo 读数据库
                       'name': info.name,
                       'image': result['head_image'],
                       'id':   result['id'],
                       'raw_image': raw_image,
                       'similarity': int(result['similarity']),
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

        #img = Image.open('/home/kenwood/cat.jpeg', 'r')
        #buffered = BytesIO()
        #img.save(buffered, format="JPEG")
        #img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        img_str=""
        cam_dict = {
            "map": img_str,
            "camera": [{
                "name": "摄像头A",
                "id": 1,
                "url": "http://nginx/livestream.flv",
                # "url":"http://live.useease.cn/live/livestream.flv?auth_key=1528096827-0-0-7a54cf956bee59637d10309a96b2969a",
                "x": 30,
                "y": 50
            },
                {
                    "name": "摄像头B",
                    "id": 2,
                    "url": "http://nginx/livestream.flv",
                    # "url": "http://live.useease.cn/live/livestream.flv?auth_key=1528096827-0-0-7a54cf956bee59637d10309a96b2969a",
                    "x": 70,
                    "y": 80,
            }]
        }
        self.write(cam_dict)

class GetTodayNum(tornado.web.RequestHandler):



    def post(self, *args, **kwargs):
        today = self.get_argument('today')
        print ('today',today)
        result = recoginiton.get_today_nums(today)
        self.write(result)

class GetLastWeek(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        date = self.get_argument('date')
        result = recoginiton.get_last_week(date)
        self.write(result)

#fake data
class GetCamNum(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        fake_data ={'online':4,
                    'outline':2,
                    'total':6}
        self.write(fake_data)

def make_app():
    return tornado.web.Application([
        (r"/get_camera", CamHandler),
        (r'/live', SocketHandler),
        (r'/get_today_num',GetTodayNum),
        (r'/get_last_week',GetLastWeek),
        (r'/get_cam_num',GetCamNum),
    ])

def main():
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(5000)
    server.start(0)  # forks one process per cpu
    IOLoop.current().start()

if __name__ == '__main__':
    main()
