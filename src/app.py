# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS

from utils import redis_queue

q = redis_queue.RedisQueue('rq')

app = Flask(__name__)
CORS(app)



#
# @app.route('/')
# def index():
#     return render_template('examples.html')


@app.route('/get_data')
def get_data():
    result_list = []
    # for i in range(1,5):
    data = q.get_nowait().decode('utf-8')
    result = eval(data)
    result_list.append(result)
    return jsonify(result_list)


# @app.route('/video/<string:file_name>')
# def stream(file_name):
#     video_dir = './video'
#     return send_from_directory(directory=video_dir, filename=file_name)


if __name__ == '__main__':
    app.run('0.0.0.0')