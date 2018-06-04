


from src.FaceRecognition.faceNet.faceNetRecognition import faceNetRecognition
import cv2
import datetime
from PIL import Image
from src.Config.Config import Config

from src.FaceDetection.MTCNNDetection import MTCNNDetection
from src.FaceFeature.FaceNet.FaceNetExtract import FaceNetExtract

from src.DrawPicture.DrawFace import Draw

from src.library.faceNetLib.faceNetFeatureLib import faceNetLib
import  base64
from io import  BytesIO




# q = RedisQueue(name="sb",host='192.168.0.245', port=6379, db=0) #RedisQueue('rq')  # 新建队列名为rq
src = "rtsp://admin:qwe123456@192.168.0.202:554/cam/realmonitor?channel=1&subtype=0"

vidwo_path ="E:/优异科技/人类识别数据检测平台/人脸识别项目Git管理/20180531.mp4"

src1807 = "rtsp://admin:qwe123456@192.168.1.202:554/cam/realmonitor?channel=1&subtype=0"
video_capture = cv2.VideoCapture(0)

#
conf = Config("./Config/config.ini")
#
# # ** 构建人脸特征库对象
# facelib = faceNetLib(conf)
#
# known_face_dataset = facelib.getlib()  #人脸特征库
#
#
# Recognition = faceNetRecognition()  # 人脸识别接口
faceDetect = MTCNNDetection(conf)  # 人脸 检测接口
faceFeature = FaceNetExtract(conf) # 人脸特征抽取接口
draw =Draw(conf)
jump = True
#
# CACHE = set()

count =0

while True:
    if jump:



        # 获取一帧视频
        ret, frame = video_capture.read()
        saveframe = frame
        #Todo 判断那一帧进入识别流程

        count += 1
        if count < 3500:
            continue

        #
        # # 人脸检测:
        # # locations：人脸位置。  landmarks：人脸特征点
        locations, landmarks = faceDetect.detect(frame)
        #

        # # ** 人脸特征抽取
        # features_arr：人脸特征    positions：人脸姿态
        features_arr, positions = faceFeature.Extract(frame,locations, landmarks)
        #
        # # ** 人脸识别/特征比对
        # face_id = Recognition.Recognit(known_face_dataset, features_arr, positions)
        #
        # [ymin, xmin, ymax, xmax]

        face_imgs = draw.drawFacebyLocation(frame,locations) #draw.DrawFace(frame,locations,landmarks)

        # 画框
        for location in locations:
            # [ymin, xmin, ymax, xmax]
            ymin = location[0]
            xmin = location[1]
            ymax = location[2]
            xmax = location[3]

            cv2.rectangle(frame, (xmin, ymax), (xmax, ymin), (255, 0, 0))


        for head in face_imgs:


            cv2.imshow("test", head)
            cv2.waitKey(1)

            # head = frame[xmin:xmax, ymax:ymin]
            #
            # cv2.imshow("test", head)
            # cv2.waitKey(1)


        # Hit 'q' on the keyboard to quit!




    jump = not jump
