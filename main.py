# coding:utf-8


from src.FaceRecognition.faceNet.faceNetRecognition import faceNetRecognition
import cv2
import datetime
from PIL import Image
from src.Config.Config import Config
from src.utils.redis_queue import RedisQueue
from src.FaceDetection.MTCNNDetection import MTCNNDetection
from src.FaceFeature.FaceNet.FaceNetExtract import FaceNetExtract
from src.library.faceNetLib.faceNetFeatureLib import faceNetLib
import  base64
from io import  BytesIO

from src.service import  recoginiton as recoginitionDB

from src.service import  camframe as camframeDB

q = RedisQueue('rq',host='192.168.0.245', port=6379, db=0)  # 新建队列名为rq
src = "rtsp://admin:qwe123456@192.168.0.202:554/cam/realmonitor?channel=1&subtype=0"
video_capture = cv2.VideoCapture(src)
video_capture.set(cv2.CAP_PROP_POS_FRAMES,25)



conf = Config("./src/Config/config.ini")

# ** 构建人脸特征库对象
facelib = faceNetLib(conf)

known_face_dataset = facelib.getlib()  #人脸特征库


Recognition = faceNetRecognition()  # 人脸识别接口
faceDetect = MTCNNDetection(conf)  # 人脸 检测接口
faceFeature = FaceNetExtract(conf) # 人脸特征抽取接口
jump = True

CACHE = set()




while True:
    if jump:


        # 获取一帧视频
        ret, frame = video_capture.read()
        saveframe = frame
        #Todo 判断那一帧进入识别流程


        # 人脸检测:
        # locations：人脸位置。  landmarks：人脸特征点
        locations, landmarks = faceDetect.detect(frame)

        # ** 人脸特征抽取
        # features_arr：人脸特征    positions：人脸姿态
        features_arr, positions = faceFeature.Extract(frame,locations, landmarks)

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


        #
        # cv2.imshow("test", frame)
        # cv2.waitKey(0)
        # Hit 'q' on the keyboard to quit!




        """frame 转图片,base64编码"""
        img = Image.fromarray(frame, 'RGB')
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")


        result_dict = {}
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for (id, simi) in face_id[0]:

            if id in CACHE:
                pass
                # continue


            CACHE.add(id)
            result_dict['ts'] = time
            result_dict['name'] = id  # list
            result_dict['image'] = img_str  # list
            result_dict['raw_image'] = img_str  # list
            result_dict['similarity'] = simi  # list
            print(result_dict['name'])
            q.put(result_dict)

        # if face_id:
        #     # import pdb
        #     # pdb.set_trace()
        #     result_dict['ts'] = time
        #     result_dict['name'] = redi_names  # list
        #     result_dict['image'] = redi_images # list
        #     result_dict['raw_image'] = redi_images  # list
        #     result_dict['similarity'] = redi_sim  #  list
        #     print(result_dict)
        #     q.put(result_dict)


    jump = not jump

