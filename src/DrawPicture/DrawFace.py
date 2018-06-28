

from src.FaceFeature.FaceNet.align_custom import AlignCustom
from src.FaceFeature.FaceNet.faceNet_feature import FaceFeature
from src.FaceRecognition.faceNet.tf_graph import FaceRecGraph

class ImageUtil():
    '''
    图片操作类，
    获取图片中的头像
    '''

    def __init__(self,conf):
        FRGraph = FaceRecGraph()

        self._aligner = AlignCustom()


    def getFaceImgbyLocation(self, image, locations):

        result =[]

        image_shape = image.shape

        Image_Xmax = image[0]
        Image_Ymax = image[1]

        X_rate = int(Image_Xmax * 0.1)
        Y_rate = int(Image_Ymax * 0.1)

        for location in locations:




            ymax = location[0] + Y_rate
            xmin = location[1] - X_rate
            ymin = location[2] - Y_rate
            xmax = location[3] + X_rate

            if ymin<0:
                ymin = 0
            if xmin<0:
                xmin = 0
            if xmax>Image_Xmax:
                xmax = Image_Xmax
            if ymax > Image_Ymax:
                ymax = Image_Ymax

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
