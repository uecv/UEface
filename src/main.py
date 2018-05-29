# coding:utf-8

import base64
import datetime
from io import BytesIO
import cv2
from PIL import Image
from src.Config.Config import Config
from src.FaceDetection.MTCNNDetection import MTCNNDetection
from src.FaceFeature.FaceNet.FaceNetExtract import FaceNetExtract
from src.FaceRecognition.faceNet.faceNetRecognition import faceNetRecognition
from src.library.faceNetLib.faceNetFeatureLib import faceNetLib
from src.util.redis_queue import RedisQueue

q = RedisQueue('rq')  # 新建队列名为rq
src = "rtsp://admin:qwe123456@192.168.0.202:554/cam/realmonitor?channel=1&subtype=0"
video_capture = cv2.VideoCapture(0)
conf = Config("./Config/config.ini")
# ** 构建人脸特征库对象
facelib = faceNetLib(conf)
known_face_dataset = facelib.getlib()  # 人脸特征库
Recognition = faceNetRecognition()  # 人脸识别接口
faceDetect = MTCNNDetection(conf)  # 人脸 检测接口
faceFeature = FaceNetExtract(conf)  # 人脸特征抽取接口
jump = True

while True:
    if jump:
        # 获取一帧视频
        ret, frame = video_capture.read()
        saveframe = frame
        # Todo 判断那一帧进入识别流程
        # 人脸检测:
        # locations：人脸位置。  landmarks：人脸特征点
        locations, landmarks = faceDetect.detect(frame)
        # ** 人脸特征抽取
        # features_arr：人脸特征    positions：人脸姿态
        features_arr, positions = faceFeature.Extract(frame, locations, landmarks)
        # ** 人脸识别/特征比对
        face_id = Recognition.Recognit(known_face_dataset, features_arr, positions)
        #
        # cam = camframeDB.Camframe(1,saveframe)
        # camframeDB.insert_camframe(cam)

        # for id in face_id:
        #     if id !="Unknown":
        #         dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #         reco = recoginitionDB.Recoginition(saveframe,1,cam.id,id,dt)
        #         recoginitionDB.insert_result(reco)

        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.imshow("test", frame)
        cv2.waitKey(0)
        # Hit 'q' on the keyboard to quit!
        """frame 转图片,base64编码"""
        img = Image.fromarray(frame, 'RGB')

        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        result_dict = {}
        if face_id:
            # import pdb
            # pdb.set_trace()
            result_dict['ts'] = time
            result_dict['name'] = face_id[0]
            result_dict['image'] = img_str
            result_dict['raw_image'] = img_str
            result_dict['similarity'] = face_id[1]
            print(result_dict)
            q.put(result_dict)

    jump = not jump
