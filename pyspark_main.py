#!/usr/bin/env python 
# coding: utf-8 
""" 
   @author: kenwood
   @time: 18-6-6 下午5:15  
"""
import base64
import datetime
import uuid
from io import BytesIO
import  numpy as np
import cv2
from PIL import Image
from src.Config import Config
from src.FaceDetection.MTCNNDetection import MTCNNDetection
from src.FaceFeature.FaceNet.FaceNetExtract import FaceNetExtract
from src.FaceRecognition.faceNet.faceNetRecognition import faceNetRecognition
from src.library.faceNetLib.faceNetFeatureLib import faceNetLib
from src.utils.redis_queue import RedisQueue
from src.utils import log,Constant
from src.DrawPicture.DrawFace import ImageUtil
from src.Config.settings import faceLibPath,mtcnnDeteModel,faceNetModel
from pyspark import SparkContext,SparkConf
from pyspark.streaming import StreamingContext
from kafka import KafkaConsumer

#create spark context
conf = (SparkConf().setAppName("PythonSparkStreamingKafka"))
sc = SparkContext(conf=conf)
sc.setLogLevel("WARN")
scc = StreamingContext(sc,6)





def main_func(id):
    LOG = log.log()
    LOG.debug('this is a test')
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
    # 构建人脸特征库对象
    facelib = faceNetLib(conf)
    # 人脸特征库
    known_face_dataset = facelib.getlib()

    # 人脸识别接口
    Recognition = faceNetRecognition()
    # 人脸 检测接口
    faceDetect = MTCNNDetection(conf)
    # 人脸特征抽取接口
    faceFeature = FaceNetExtract(conf)

    # pickle.dump(Recognition,open('RecognitionMODEL.pickle','wb'))

    imageUtil = ImageUtil()  # 人脸抠图的接口

    jump = True

    dist_name_num = {}

    countFrame = 0

    def addFrame2Cach(face_id, face_image, dist_id_num):
        '''
        1、将每一帧的结果保存到dist_name_num中。
        2、根据时间判断是否清除缓存dist_name_num
        :param face_id:list
        :param locations:
        :param start_time:
        :param dist_name_num:dict
        :return:
        '''

        for id_simi, img in zip(face_id, face_image):

            id, simi = id_simi

            if id not in dist_id_num:
                dist_id_num[id] = [1, [img], [simi]]
            else:
                k = dist_id_num[id][0]
                dist_id_num[id][0] = dist_id_num[id][0] + 1
                dist_id_num[id][1].append(img)
                dist_name_num[id][2].append(simi)

    def filterByCach(dist_name_num):

        web_faceid = []

        web_faceimg = []

        for id in dist_name_num:

            num, head_images, simis = dist_name_num[id]

            resultsimis = np.mean(simis)

            maxsimi_index = simis.index(max(simis))

            result_head = head_images[maxsimi_index]

            if num > 10:
                web_faceid.append((id, resultsimis))
                LOG.debug('{},{}'.format(id, resultsimis))
                web_faceimg.append(result_head)

        return web_faceid, web_faceimg

    consumer = KafkaConsumer('frame',
                                 bootstrap_servers=['192.168.0.251:9092'], api_version=(0, 10), group_id='spark')
    for message in consumer:
        #print("%s:%d:%d: key=%s " % (message.topic, message.partition,
                                         # message.offset, message.key))

        kafka_data = message.value  # byte values of the image
        imgdata = base64.b64decode(eval(kafka_data)['data'])
        new_frame = np.asarray(Image.open(BytesIO(imgdata)))

        # 获取一帧视频
        # start_time = datetime.datetime.now()
        # ret, frame = video_capture.read()
        frame = cv2.cvtColor(new_frame, cv2.COLOR_BGR2RGB)

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

            # ==== 删除掉侧脸的头像 =====

            newlocation = []
            newPosition = []
            newFeature = []

            for location, position, feature in zip(locations, positions, features_arr):

                if position == "Center":
                    newlocation.append(location)
                    newPosition.append(position)
                    newFeature.append(feature)

            locations = newlocation
            positions = newPosition
            features_arr = newFeature

            # """frame 转图片,base64编码"""
            # img = Image.fromarray(frame, 'RGB')
            # buffered = BytesIO()
            # img.save(buffered, format="JPEG")
            # img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

            result_dict = {}
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            head_imgs = imageUtil.getFaceImgbyLocation(frame, locations)

            addFrame2Cach(face_id, head_imgs, dist_name_num)

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

            countFrame += 1
            clear = countFrame > 25
            # print(countFrame)

            if clear:

                web_ids, web_headimages = filterByCach(dist_name_num)

                for (id_simi, head_image) in zip(web_ids, web_headimages):
                    id, simi = id_simi
                    if id == "Unknown":
                        continue
                    if redis_connect.exists_key(id):
                        LOG.debug('exitst key')
                        continue
                    LOG.debug('not running')
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
                    result_dict['similarity'] = int(simi * 100)  # list
                    LOG.debug(result_dict['user_id'])
                    # print (result_dict)
                    redis_connect.put(redis_queue, result_dict)

                dist_name_num = {}  # 清空缓存

                countFrame = 0  # 重新开始计数


sc.parallelize(range(1,3)).foreachPartition(main_func)



