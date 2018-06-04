# coding:utf-8


import base64
import datetime
import uuid
from io import BytesIO

import cv2
from PIL import Image
from src.Config import Config
from src.FaceDetection.MTCNNDetection import MTCNNDetection
from src.FaceFeature.FaceNet.FaceNetExtract import FaceNetExtract
from src.FaceRecognition.faceNet.faceNetRecognition import faceNetRecognition
from src.library.faceNetLib.faceNetFeatureLib import faceNetLib
from src.utils.redis_queue import RedisQueue
from src.utils import Constant
from src.DrawPicture.DrawFace import Draw

redis_connect = RedisQueue(
    host='192.168.0.245',
    port=6379)

src = "rtsp://admin:qwe123456@192.168.1.202:554/cam/realmonitor?channel=1&subtype=0"
video_capture = cv2.VideoCapture(src)
# video_capture.set(cv2.CAP_PROP_POS_FRAMES,25)
conf = Config.Config(Constant.CONFIG_PATH)
redis_host = conf.get('web', 'redis_host')
redis_port = conf.get('web', 'redis_port')
redis_queue = conf.get('web', 'redis_queue')
image_path = conf.get('web', 'image_root')
map_path = conf.get('web', 'map_path')
# ** 构建人脸特征库对象
facelib = faceNetLib(conf)
# 人脸特征库
known_face_dataset = facelib.getlib()

# 人脸识别接口
Recognition = faceNetRecognition()
# 人脸 检测接口
faceDetect = MTCNNDetection(conf)
# 人脸特征抽取接口
faceFeature = FaceNetExtract(conf)

draw = Draw(conf)                    # 人脸抠图的接口

jump = True


while True:
    if jump:
        # 获取一帧视频
        start_time = datetime.datetime.now()
        ret, frame = video_capture.read()
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

        # Todo 判断那一帧进入识别流程

        # 人脸检测:
        # locations：人脸位置。  landmarks：人脸特征点
        locations, landmarks = faceDetect.detect(frame)
        if locations:

            # ** 人脸特征抽取
            # features_arr：人脸特征    positions：人脸姿态
            features_arr, positions = faceFeature.Extract(
                frame, locations, landmarks)

            # ** 人脸识别/特征比对
            face_id = Recognition.Recognit(
                known_face_dataset, features_arr, positions)

            #Todo 原始帧
            # """frame 转图片,base64编码"""
            # img = Image.fromarray(frame, 'RGB')
            # buffered = BytesIO()
            # img.save(buffered, format="JPEG")
            # img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

            result_dict = {}
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            head_imgs = draw.drawFacebyLocation(frame,locations)



            # 画框
            #############调试代码########################
            # for location in locations:
            #     # [ymin, xmin, ymax, xmax]
            #     ymin = location[0]
            #     xmin = location[1]
            #     ymax = location[2]
            #     xmax = location[3]
            #
            #     cv2.rectangle(frame, (xmin, ymax), (xmax, ymin), (255, 0, 0))
            # cv2.imshow("test", frame)
            # cv2.waitKey(1)
            ###############################################

            for (id_simi,head_image) in zip(face_id[0],head_imgs):
                id, simi=id_simi
                if id == "Unknown":
                    continue
                if redis_connect.exists_key(id):
                    continue

                head_img = Image.fromarray(head_image, 'RGB')
                buffered = BytesIO()
                head_img.save(buffered, format="JPEG")
                img_head_str = base64.b64encode(buffered.getvalue()).decode("utf-8")


                # CACHE.add(id)
                redis_connect.time_key(id, simi, 20)
                result_dict['id'] = str(uuid.uuid4())
                result_dict['ts'] = time
                result_dict['user_id'] = id  # list
                result_dict['head_image'] = img_head_str  # list
                result_dict['similarity'] = int(simi)  # list
                print(time,result_dict['user_id'])
                redis_connect.put(redis_queue,result_dict)

    jump = not jump
