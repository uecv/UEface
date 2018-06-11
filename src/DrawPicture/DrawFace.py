

from src.FaceFeature.FaceNet.align_custom import AlignCustom
from src.FaceFeature.FaceNet.faceNet_feature import FaceFeature
from src.FaceRecognition.faceNet.tf_graph import FaceRecGraph
from PIL import  Image
import matplotlib.pyplot as plt

class Draw():
    '''
    图片操作类，
    获取图片中的头像
    '''

    def __init__(self,conf):
        FRGraph = FaceRecGraph()

        self._aligner = AlignCustom()


    def drawFacebyLocation(self,image,locations):

        result =[]


        for location in locations:
            ymin = location[0]-5
            xmin = location[1]-5
            ymax = location[2]+5
            xmax = location[3]+5

            # box = (xmin,ymax,xmax,ymin)
            # pil_image = Image.fromarray(image)
            # head = pil_image.crop(box)

            head =image[ymax:ymin,xmin:xmax]

            result.append(head)
        return result


    def DrawFace(self,image, locations,landmarks):
        # 坐标点转换，将[ymin, xmin, ymax, xmax] 格式转换为 [xmin,ymax,w,h]格式
        rects = []
        for i in locations:
            xmin = i[1]
            ymax = i[2]
            w = i[3] - xmin
            h = i[0] - ymax
            rects.append([xmin, ymax, w, h])

        aligns = []

        for (i, rect) in enumerate(rects):

            aligned_face, face_pos = self._aligner.align(
                160, image, landmarks[i])
            if len(aligned_face) == 160 and len(aligned_face[0]) == 160:

                aligns.append(aligned_face)

            else:
                print("Align face failed")  # log

        return aligns
