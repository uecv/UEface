# coding:utf-8
import datetime

from src.DrawPicture.tensorflow_draw_location.draw_face_box import draw_box
from src.FaceRecognition.faceNet.faceNetRecognition import faceNetRecognition


def recognition(frame, EncodingCache, known_face_dataset):
    """

    :param frame: np array
    :param EncodingCache: empty list
    :param known_face_dataset:
    :return:
    """

    # 获取该图片下所有人脸的位置和编码　
    #Todo 编码意思？

    Recognition = faceNetRecognition()

    face_locations, face_encodings, positions, image = Recognition.face_locations_encoding(
        frame)

    # 将人脸编码添加到缓存中
    for face in face_encodings:
        EncodingCache.append(face)

    face_names = []
    # start(EncodingCache, face_encodings):  # 如果达到判断人脸的条件
    if face_locations:

        face_names = Recognition.findPeople(
            face_encodings, positions, data_set=known_face_dataset)

        frame = draw_box(frame, face_locations)

    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在

    return (frame, face_names, nowTime, image)
