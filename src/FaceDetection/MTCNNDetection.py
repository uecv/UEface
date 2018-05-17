
from src.Config.FaceNetconfig import  config

'''MTCNN模型  人脸检测类，
'''


class MTCNNDetection:

    def __init__(self):
        con = config()
        self.detectonModel = con.getdetectionModel()


    def detect(self,image):
        '''
        人脸检测接口
        :param images:
        :return: 返回照片中人脸的位置 ,以及特征点
        '''

        rects, landmarks = self.detectonModel.detect_face(image, 80);  # min face size is set to 80x80
        locations = []
        for (i, rect) in enumerate(rects):
            xmin = rect[0]
            ymax = rect[1]
            xmax = rect[0] + rect[2]
            ymin = rect[1] + rect[3]
            locations.append([ymin, xmin, ymax, xmax])

        return locations,landmarks