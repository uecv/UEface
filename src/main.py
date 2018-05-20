# coding:utf-8

import base64
import json
from io import BytesIO

import cv2
from PIL import Image
from src.FaceRecognition import old_faceRecognition
from src.util.redis_queue import RedisQueue

q = RedisQueue('rq')  # 新建队列名为rq
src = "rtsp://admin:qwe123456@192.168.0.202:554/cam/realmonitor?channel=1&subtype=0"
video_capture = cv2.VideoCapture(0)


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


EncodingCache = []  # 用于存储一段时间内脸部编码的缓存

#### Todo ????
f = open('./Model/faceNet/facerec_128D.txt', 'r')
known_face_dataset = json.loads(f.read())
f.close()



def main():
    frame_number = 0
    while True:
        frame_number += 1
        # 获取一帧视频
        ret, frame = video_capture.read()
        #Todo 判断那一帧进入识别流程


        #Todo 注释
        (frame, face_names, now_time, image) = old_faceRecognition.recognition(
            frame, EncodingCache, known_face_dataset)


        # cv2.imshow("test", frame)
        # Hit 'q' on the keyboard to quit!
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

        """frame 转图片,base64编码"""
        img = Image.fromarray(frame, 'RGB')
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        result_dict = {}
        if face_names:
            # import pdb
            # pdb.set_trace()
            result_dict['time'] = now_time
            result_dict['name'] = face_names
            result_dict['image'] = img_str
            print(result_dict)
            # q.put(result_dict)

if __name__ == '__main__':
    #Todo?
    main()
