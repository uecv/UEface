#!/usr/bin/env python 
# coding: utf-8 
""" 
   @author: kenwood
   @time: 18-5-29 上午9:34  
"""
import tornado.ioloop
import tornado.web
import tornado.websocket
from PIL import Image
from io import BytesIO
import base64

cl = []
class SocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        if self not in cl:
            cl.append(self)

    def on_message(self,message):
        print ('test')
        self.write_message(u"You said: ")

    def on_close(self):
        if self in cl:
            cl.remove(self)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
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


if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r'/ws', SocketHandler),
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()