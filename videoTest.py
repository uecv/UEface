# coding=utf-8


import time

import cv2
import pinyin

from src.Config.Config import Config
from src.DrawPicture.DrawFace import ImageUtil
from src.FaceDetection.MTCNNDetection import MTCNNDetection
from src.FaceFeature.FaceNet.FaceNetExtract import FaceNetExtract
from src.FaceRecognition.faceNet.faceNetRecognition import faceNetRecognition
from src.library.faceNetLib.faceNetFeatureLib import faceNetLib
from src.service.people import get_people

# q = RedisQueue(name="sb",host='192.168.0.245', port=6379, db=0) #RedisQueue('rq')  # 新建队列名为rq
src = "rtsp://admin:qwe123456@192.168.0.202:554/cam/realmonitor?channel=1&subtype=0"

vidwo_path = "E:/优异科技/人类识别数据检测平台/人脸识别项目Git管理/testVedio.mp4"
video_path_245 = "testVedio.mp4"
src1807 = "rtsp://admin:qwe123456@192.168.1.202:554/cam/realmonitor?channel=1&subtype=0"
video_capture = cv2.VideoCapture(video_path_245)
video_capture.set(cv2.CAP_PROP_FPS, 10)
#
conf = Config("./src/Config/config.ini")
#
# # ** 构建人脸特征库对象
facelib = faceNetLib(conf)
#
known_face_dataset = facelib.getlib()  # 人脸特征库
#
#
Recognition = faceNetRecognition(conf)  # 人脸识别接口 RandomForestRecognition(conf)     #
faceDetect = MTCNNDetection(conf)  # 人脸 检测接口
faceFeature = FaceNetExtract(conf)  # 人脸特征抽取接口
draw = ImageUtil(conf)

#
# CACHE = set()

COUNT = 0

# 获得码率及尺寸
fps = video_capture.get(cv2.CAP_PROP_FPS)
size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
fourcc = cv2.VideoWriter_fourcc("X", "V", "I", "D")
# 指定写视频的格式, I420-avi, MJPG-mp4
videoWriter = cv2.VideoWriter('recognition_5000.mp4', fourcc, fps, size)

while True:

    luyupath = "./src/library/images/卢宇_003.png"
    videopath = "test.jpg"

    # 获取一帧视频
    ret, frame = video_capture.read()

    start_time = time.time()
    # # frame = cv2.medianBlur(frame,3)
    # blurred = np.hstack([cv2.medianBlur(frame, 3),
    #                      cv2.medianBlur(frame, 5),
    #                      cv2.medianBlur(frame, 7)
    #                      ])
    # cv2.imshow("Median", blurred)
    # # cv2.imshow("test", frame)
    # cv2.waitKey(1)
    # continue

    # saveframe = frame
    # frame = cv2.imdecode(np.fromfile(videopath, dtype=np.uint8), -1)
    # Todo 判断那一帧进入识别流程

    # count += 1
    # if count < 5000:
    #     print(count)
    #     continue

    #
    # # 人脸检测:
    # # locations：人脸位置。  landmarks：人脸特征点
    locations, landmarks = faceDetect.detect(frame)

    t1 = (time.time() - start_time)

    # print("人脸检测时间 {t1}" )
    # print(t1)

    #
    # 判断人脸位置是否模糊
    # vague =[]  #　１：模糊　　０：正常
    # for location in locations:
    #     ymin = location[0]
    #     xmin = location[1]
    #     ymax = location[2]
    #     xmax = location[3]
    #     head = frame[ymax:ymin, xmin:xmax]
    #     img2gray = cv2.cvtColor(head, cv2.COLOR_BGR2GRAY)  # 将图片压缩为单通道的灰度图
    #     score = cv2.Laplacian(img2gray, cv2.CV_64F).var()
    #     if score<100:
    #         vague.append(1)
    #     else:
    #         vague.append(0)




    #   ** 人脸特征抽取
    # features_arr：人脸特征    positions：人脸姿态
    features_arr, positions = faceFeature.Extract(frame, locations, landmarks)

    t2 = (time.time() - start_time)

    # print("到达人脸特征抽取的时间 {t2}")
    # print(t2)
    # newFeature =[]
    # newPosition =[]
    # newLocations = []
    # for position,feature,location in zip(positions,features_arr,locations):
    #     if position == 'Center':
    #         newFeature.append(feature)
    #         newLocations.append(location)
    #         newPosition.append(position)
    # features_arr = newFeature
    # positions = newPosition
    # locations = newLocations
    start_time = time.time()
    #
    # # ** 人脸识别/特征比对
    face_id = Recognition.Recognit(known_face_dataset, features_arr, positions)

    t3 = (time.time() - start_time)
    # print("到达人脸验证花费的时间{t3}")
    # print(t3)
    # print(face_id)

    names = []

    for temp in face_id:
        id, simi = temp
        name = "unknown"
        if id != "Unknown":
            name, img_path = get_people(id)
            name = pinyin.get(name, format="strip", delimiter=" ")
        names.append(name)
    # [ymin, xmin, ymax, xmax]




    face_imgs = draw.getFaceImgbyLocation(frame, locations)  # draw.DrawFace(frame,locations,landmarks)

    # 画框
    for location, id in zip(locations, names):
        print(names)

        # [ymin, xmin, ymax, xmax]
        ymin = location[0]
        xmin = location[1]
        ymax = location[2]
        xmax = location[3]

        cv2.rectangle(frame, (xmin, ymax), (xmax, ymin), (255, 0, 0))
        font = cv2.FONT_HERSHEY_SIMPLEX  # 定义字体
        #

        frame = cv2.putText(frame, str(id), (xmin, ymax), font, 1.2, (255, 255, 255), 2)
        # frame = cv2.putText(frame, str(va), (xmin, ymax+10), font, 1.2, (255, 255, 255), 2)
        # for head in face_imgs:


        """frame 转图片,base64编码"""
        # img = Image.fromarray(head, 'RGB')
        # img.show()

    # print(face_id)
    videoWriter.write(frame)  # 写视频帧
    # cv2.imshow("test", frame)
    # cv2.waitKey(1)
    #
    #
    #
    #
    #
    #     # head = frame[xmin:xmax, ymax:ymin]
    #     #
    # # cv2.imshow("test", frame)
    # # cv2.waitKey(1)
    #
    #
    # # Hit 'q' on the keyboard to quit!
