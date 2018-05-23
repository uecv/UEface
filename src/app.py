# -*- coding: utf-8 -*-

import base64
import datetime
from io import BytesIO
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from PIL import Image
# from src.utils import redis_queue
import json
import os
# q = redis_queue.RedisQueue('rq')
async_mode = None

app = Flask(__name__)
cors = CORS(app, resources={r"/socket.io/*": {"origins": "*"}})
socketio = SocketIO(app, async_mode=async_mode)


@app.route('/')
def get_homepage():
    return render_template('websock.html')


@app.route('/get_camera', methods=['GET'])
def get_camera():
    cam_dict = {
        "map": "xxxxxxxxxxx",
        "camera": [{
            "name": "摄像头A",
            "id": 1,
            "url": "192.168.0.245:8888/live/livestream.flv",
            "x": 1,
            "y": 2
        },
            {
            "name": "摄像头B",
            "id": 1,
            "url": "http://192.168.0.245:8888/live/livestream2.flv",
            "x": 3,
            "y": 5
        }]
    }
    return jsonify(cam_dict)


@socketio.on('my_ping', namespace='/test')
def ping_pong():
    msg = {
        "head": {
            "type": "GET_COUNT",
            "statu": 200
        },
        "body": {
            "NUMS": "50"
        }
    }
    # print('msg', msg)
    send(msg, json=True)


@socketio.on('my_result', namespace='/test')
def get_data():
    # front_time = request.form.get('front_time')
    now_time = datetime.datetime.strftime(
        datetime.datetime.today(), '%Y-%m-%d %H:%M:%S')
    img = Image.open('/home/kenwood/图片/cat.jpeg', 'r')
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    result_dict = {}
    result_list = []
    # for i in range(1, 5):
    result_dict['body'] = {
        'ts': now_time,
        'name': 'kenwood',
        'image': img_str,
        'raw_image': img_str,
        'similarity': '90%'}
    result_dict['head'] = {"type": "GET_RECO_RESULT", "statu": 200}
    # result_list.append(result_dict)
    # return jsonify(result_list)
    # for i in range(1,5):
    # data = q.get_nowait().decode('utf-8')
    # result = eval(result_dict)
    print('result_dict',result_dict)

    emit(result_dict)


@app.route('/get_time', methods=['GET', 'POST'])
def get_time():
    if request.method == "GET":
        now_time = datetime.datetime.strftime(
            datetime.datetime.today(), '%Y-%m-%d %H:%M:%S')
        return jsonify(now_time)


# @app.route('/video/<string:file_name>')
# def stream(file_name):
#     video_dir = './video'
#     return send_from_directory(directory=video_dir, filename=file_name)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
