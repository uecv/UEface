# -*- coding: utf-8 -*-

import base64
import datetime
import json
import os
import time
from datetime import timedelta
from functools import update_wrapper
from io import BytesIO

# from flask_sockets import Sockets
from flask import Flask, jsonify, make_response, render_template, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from PIL import Image
from src.utils.redis_queue import RedisQueue

q = RedisQueue('rq', host='192.168.0.245', port=6379, db=0)
async_mode = None

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "True"}},
            headers="Content-Type")
socketio = SocketIO(app, async_mode=async_mode)


# def crossdomain(origin=None, methods=None, headers=None,
#                 max_age=21600, attach_to_all=True,
#                 automatic_options=True):
#     if methods is not None:
#         methods = ', '.join(sorted(x.upper() for x in methods))
#     if headers is not None and not isinstance(headers, str):
#         headers = ', '.join(x.upper() for x in headers)
#     if not isinstance(origin, str):
#         origin = ', '.join(origin)
#     if isinstance(max_age, timedelta):
#         max_age = max_age.total_seconds()
#
#     def get_methods():
#         if methods is not None:
#             return methods
#
#         options_resp = current_app.make_default_options_response()
#         return options_resp.headers['allow']
#
#     def decorator(f):
#         def wrapped_function(*args, **kwargs):
#             if automatic_options and request.method == 'OPTIONS':
#                 resp = current_app.make_default_options_response()
#             else:
#                 resp = make_response(f(*args, **kwargs))
#             if not attach_to_all and request.method != 'OPTIONS':
#                 return resp
#
#             h = resp.headers
#
#             h['Access-Control-Allow-Origin'] = origin
#             h['Access-Control-Allow-Methods'] = get_methods()
#             h['Access-Control-Max-Age'] = str(max_age)
#             if headers is not None:
#                 h['Access-Control-Allow-Headers'] = headers
#             return resp
#
#         f.provide_automatic_options = False
#         return update_wrapper(wrapped_function, f)
#     return decorator


@app.route('/')
def get_homepage():
    return render_template('websock.html')

# @sockets.route('/echo')
# def echo_socket(ws):
#     while not ws.closed:
#         message = ws.receive()
#         new_message =json.dumps({'data':'test'})
#         ws.send(new_message)


@app.route('/get_camera', methods=['GET'])
def get_camera():
    img = Image.open('/home/kenwood/cat.jpeg', 'r')
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
    return jsonify(cam_dict)


@socketio.on("my_ping", namespace='/echo')
def ping_pong():
    msg = {

        "type": "GET_COUNT",
        "NUMS": "50"

    }
    emit("my_response", msg)


@socketio.on('connect', namespace='/echo')
def test_connect():
    emit('my_response', {'data': 'Connected'})


@socketio.on('disconnect', namespace='/echo')
def test_disconnect():
    print('Client disconnected')


@socketio.on('my_camera', namespace='/echo')
def get_camera_id(message):
    print(message)
    emit('my_response', message)
#     cam_id = message
#     print ('cam_id',cam_id)
#     msg = {
#     "type":"POST_CHANGE_CAM",
#     "id": cam_id
# }
#     send(msg, json=True)


@socketio.on('my_result', namespace='/echo')
def get_data():
    # front_time = request.form.get('front_time')
    # while True:
    # for i in range(1,10):
    #     time.sleep(2)
    #     now_time = datetime.datetime.strftime(
    #         datetime.datetime.today(), '%Y-%m-%d %H:%M:%S')
    #     img = Image.open('/home/kenwood/图片/cat.jpeg', 'r')
    #     buffered = BytesIO()
    #     img.save(buffered, format="JPEG")
    #     img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        # result_list = []
        # for i in range(1, 5):
        # result_dict = {
        #     'ts': now_time,
        #     'name': 'kenwood',
        #     'image': img_str,
        #     'raw_image': img_str,
        #     'similarity': '90%',
        #     'type': "GET_RECO_RESULT"}
        # # result_list.append(result_dict)
        # # return jsonify(result_list)

    for i in range(1, 5):

        data = q.get_nowait().decode('utf-8')
        if eval(data)['name']!= "Unknown"
            raw_image = q.get_value(eval(data)['name']).decode('utf-8')
            result = eval(data)
            result_dict = {'ts': result['ts'],
                           'name': result['name'],
                           'image': result['image'],
                           'raw_image': raw_image,
                           'similarity': result['similarity'],
                           'type': "GET_RECO_RESULT"}
            emit("my_response", result_dict)


# @app.route('/get_time', methods=['GET', 'POST'])
# def get_time():
#     if request.method == "GET":
#         now_time = datetime.datetime.strftime(
#             datetime.datetime.today(), '%Y-%m-%d %H:%M:%S')
#         return jsonify(now_time)


# @app.route('/video/<string:file_name>')
# def stream(file_name):
#     video_dir = './video'
#     return send_from_directory(directory=video_dir, filename=file_name)


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
