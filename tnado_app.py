#!/usr/bin/env python
# coding: utf-8
"""
   @author: kenwood
   @time: 18-5-29 上午9:34
"""
import tornado.ioloop
from tornado.ioloop import  IOLoop
import tornado.web
import tornado.httpserver
import tornado.websocket
from PIL import Image
from io import BytesIO
import base64
import time
from src.utils.redis_queue import RedisQueue
#队列
queue = RedisQueue('rq', host='192.168.0.245', port=6379, db=0)

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
            self.check_ten_seconds, 1000, io_loop=tornado.ioloop.IOLoop.instance())
        self.loop.start()

    def on_message(self, message):
        self.write_message(u"You said: " + message)
        self.last = time.time()

    def on_close(self):
        print("Client disconnected")
        self.loop.stop()

    def check_origin(self, origin):
        return True

    def check_ten_seconds(self):
        print("Just checking")

        #people_num
        msg = {
            "type": "GET_COUNT",
            "NUMS": "50"
        }
        #recognition result
        data = queue.get_nowait().decode('utf-8')
        print(eval(data)['name'])
        raw_image = queue.get_value(eval(data)['name']).decode('utf-8')
        result = eval(data)
        result_dict = {'ts': result['ts'],
                       'name': result['name'],
                       'image': result['image'],
                       'raw_image': raw_image,
                       'similarity': result['similarity'],
                       'type': "GET_RECO_RESULT"}


        if (time.time() - self.last > 10):
            self.write_message("You sleeping mate?")
            self.write_message(msg)
            self.write_message(result_dict)
            self.last = time.time()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

        img = Image.open('/home/kenwood/图片/cat.jpeg', 'r')
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        cam_dict = {
            "map": img_str,
            "camera": [{
                "name": "摄像头A",
                "id": 1,
                "url": "http://192.168.0.245:8888/live/livestream.flv",
                "x": 30,
                "y": 50
            },
                {
                    "name": "摄像头B",
                    "id": 2,
                    "url": "http://192.168.0.245:8888/live/livestream.flv",
                    "x": 70,
                    "y": 80,
            }]
        }
        self.write(cam_dict)
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r'/ws', SocketHandler),
    ])

def main():
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(8888)
    server.start(0)  # forks one process per cpu
    IOLoop.current().start()

if __name__ == '__main__':
    main()
