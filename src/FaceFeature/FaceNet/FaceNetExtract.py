





'''
faceNet 模型 人脸特征抽取类
'''
from src.FaceFeature.FaceNet.align_custom import AlignCustom
from src.FaceFeature.FaceNet.faceNet_feature import FaceFeature
from src.FaceRecognition.faceNet.tf_graph import FaceRecGraph

from src.FaceFeature.BaseFaceFeature import BaseFaceFeature

class FaceNetExtract(BaseFaceFeature):

    def __init__(self,conf):
        FRGraph = FaceRecGraph()
        self._model = FaceFeature(
            FRGraph,
            model_path=conf.get("path","faceNetModel"))
        self._aligner = AlignCustom()


    def Extract(self, image, locations, landmarks):
        '''
        输入人脸的坐标位置以及人脸特征点向量
        :param rects:  人脸坐标位置  shape = [N,4]  [ymin, xmin, ymax, xmax]
         :param landmarks:  特征点向量
         :param image : 原始照片
        :return:
        '''

        # 坐标点转换，将[ymin, xmin, ymax, xmax] 格式转换为 [xmin,ymax,w,h]格式
        rects = []
        for i in locations:
            xmin = i[1]
            ymax = i[2]
            w = i[3] - xmin
            h = i[0] - ymax
            rects.append([xmin, ymax, w, h])

        aligns = []
        positions = []
        for (i, rect) in enumerate(rects):
            aligned_face, face_pos = self._aligner.align(
                160, image, landmarks[i])
            if len(aligned_face) == 160 and len(aligned_face[0]) == 160:
                aligns.append(aligned_face)
                positions.append(face_pos)
            else:
                print("Align face failed")  # log

        features_arr = []
        if aligns:
            features_arr = self._model.get_features(aligns)

        return features_arr, positions
