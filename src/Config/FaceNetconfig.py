
from src.FaceFeature.FaceNet.align_custom import AlignCustom
from src.FaceFeature.FaceNet.faceNet_feature import FaceFeature
from src.FaceDetection.mtcnn_detect import MTCNNDetect
from src.FaceRecognition.faceNet.tf_graph import FaceRecGraph
from functools import wraps

import  os
import  src.library.faceNetLib as faceNetLib
import  src.Model.faceNet.models as models
import  src.library.images as images
import  json

def Singleton(cls):

    instances ={}
    @wraps(cls)
    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls]=cls(*args,**kwargs)
        return instances[cls]
    return getinstance



@Singleton
class config:

    def __init__(self):

        faceNetLibroot = faceNetLib.__path__[0]
        faceNetLibPath = os.path.join(faceNetLibroot,"facerec_128D.txt")  #"./library/faceNetLib/facerec_128D.txt"

        imagesRoot = images.__path__[0]

        face_model_root =  models.__path__[0] #"./Model/faceNet/models/"

        extract_feature_modelpath =   os.path.join(face_model_root,"model-20170512-110547.ckpt-250000")



        # extract_feature_modelpath ="./Model/faceNet/models/model-20170512-110547.ckpt-250000"

        self._FRGraph = FaceRecGraph()
        self._aligner = AlignCustom()
        # model_path="./Model//faceNet/models/model-20170512-110547.ckpt-250000"
        self._extract_feature = FaceFeature(self._FRGraph, model_path=extract_feature_modelpath)
        # model_path="./Model/faceNet/models/"
        self._face_detect = MTCNNDetect(self._FRGraph,model_path = face_model_root , scale_factor=2)

        self._faceNetLibPath = faceNetLibPath  # "./library/faceNetLib/facerec_128D.txt"

        self._imagePath =  imagesRoot     # "./library/images/"

        f = open(self._faceNetLibPath, 'r')
        self._known_face_dataset = json.loads(f.read())
        f.close()

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

    def getKnown_face_dataset(self):
        return self._known_face_dataset


conf = config()
