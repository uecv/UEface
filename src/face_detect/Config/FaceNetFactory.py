
from functools import wraps

from src.FaceDetection.mtcnn_detect import MTCNNDetect
from src.FaceFeature.FaceNet.align_custom import AlignCustom
from src.FaceFeature.FaceNet.faceNet_feature import FaceFeature
from src.FaceRecognition.faceNet.tf_graph import FaceRecGraph


def Singleton(cls):

    instances = {}

    @wraps(cls)
    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return getinstance


@Singleton
class FaceDetectionFactory:

    def __init__(self):
        self._FRGraph = FaceRecGraph()
        self._aligner = AlignCustom()
        self._extract_feature = FaceFeature(
            self._FRGraph,
            model_path="./Model/faceNet/models/model-20170512-110547.ckpt-250000")
        self._face_detect = MTCNNDetect(
            self._FRGraph,
            model_path="./Model/faceNet/models/",
            scale_factor=2)

        self._faceNetLibPath = "./library/faceNetLib/facerec_128D.txt"

        self._imagePath = "./library/images/"

    def getImagePath(self):
        return self._imagePath

    def getdetectionModel(self):
        return self._face_detect

    def getfaceFeatureModel(self):
        return self._extract_feature

    def getalignerModel(self):
        return self._aligner

    def getFaceNetLibPath(self):
        return self._faceNetLibPath
