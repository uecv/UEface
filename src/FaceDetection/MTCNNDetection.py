



'''MTCNN模型  人脸检测类，
'''

from src.FaceDetection.mtcnn_detect import MTCNNDetect
from src.FaceRecognition.faceNet.tf_graph import FaceRecGraph
class MTCNNDetection:

    def __init__(self,conf):

        FRGraph = FaceRecGraph()
        self.detectonModel = MTCNNDetect(
            FRGraph,
            model_path=conf.get("path","mtcnnDeteModel"),
            scale_factor=2)






    def detect(self, image):
        '''
        人脸检测接口
        :param images:
        :return: 返回照片中人脸的位置 ,以及特征点
        '''

        rects, landmarks = self.detectonModel.detect_face(
            image, 80)  # min face size is set to 80x80
        locations = []
        for (i, rect) in enumerate(rects):
            xmin = rect[0]
            ymax = rect[1]
            xmax = rect[0] + rect[2]
            ymin = rect[1] + rect[3]
            locations.append([ymin, xmin, ymax, xmax])

        return locations, landmarks
