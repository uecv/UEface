
import datetime


from src.DrawPicture.tensorflow_draw_location.draw_face_box import draw_box

from src.FaceRecognition.faceNet.faceNetRecognition import  faceNetRecognition




def recognition(frame,EncodingCache,known_face_dataset):

    # Resize frame of video to 1/4 size for faster face recognition processing
    # small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame =frame # small_frame[:, :, ::-1]

    # 获取该图片下所有人脸的位置和编码

    Recognition = faceNetRecognition()

    face_locations, face_encodings, positions,image = Recognition . face_locations_encoding(rgb_small_frame)

    # 将人脸编码添加到缓存中
    for face in face_encodings:
        EncodingCache.append(face)

    face_names = []
    if len(face_locations)>0: #start(EncodingCache, face_encodings):  # 如果达到判断人脸的条件

        face_names = Recognition .findPeople(face_encodings,positions,data_set=known_face_dataset)

        frame = draw_box(frame, face_locations)

    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在




    return (frame,face_names,nowTime,image)

