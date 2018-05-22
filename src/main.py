# coding:utf-8


from src.FaceRecognition.faceNet.faceNetRecognition import faceNetRecognition
import cv2
from src.Config.Config import Config

from src.util.redis_queue import RedisQueue
from src.FaceDetection.MTCNNDetection import MTCNNDetection
from src.FaceFeature.FaceNet.FaceNetExtract import FaceNetExtract
from src.library.faceNetLib.faceNetFeatureLib import faceNetLib
q = RedisQueue('rq')  # 新建队列名为rq
src = "rtsp://admin:qwe123456@192.168.0.202:554/cam/realmonitor?channel=1&subtype=0"
video_capture = cv2.VideoCapture(0)




# 配置文件对象
conf = Config("./Config/config.ini")

# ** 构建人脸特征库对象
facelib = faceNetLib(conf)

known_face_dataset = facelib.getlib()  #人脸特征库


Recognition = faceNetRecognition()  # 人脸识别接口
faceDetect = MTCNNDetection(conf)  # 人脸 检测接口
faceFeature = FaceNetExtract(conf) # 人脸特征抽取接口
jump = True


while True:
    if jump:

        # 获取一帧视频
        ret, frame = video_capture.read()


        # 人脸检测:
        # locations：人脸位置。  landmarks：人脸特征点
        locations, landmarks = faceDetect.detect(frame)

        # ** 人脸特征抽取
        # features_arr：人脸特征    positions：人脸姿态
        features_arr, positions = faceFeature.Extract(frame,locations, landmarks)

        # ** 人脸识别/特征比对
        face_id = Recognition.Recognit(known_face_dataset, features_arr, positions)




        print(face_id)

        cv2.imshow("test", frame)
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # continue

    jump = not jump
