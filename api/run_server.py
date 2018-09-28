#!/usr/bin/env python 
# coding: utf-8 
""" 
   @author: kenwood
   @time: 18-8-21 下午2:27  
"""
import tornado.web
import tornado.httpserver
from tornado.ioloop import IOLoop
from api.handler.face_detect import facedecetehandler
from api.handler.add_face import addfacehandler



def make_app():
    return tornado.web.Application([
        (r"/face_detect", facedecetehandler),
        (r'/add_face', addfacehandler),
    ])

def main():
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(5000)
    server.start(0)  # forks one process per cpu
    IOLoop.current().start()

if __name__ == '__main__':
    main()