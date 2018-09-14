from src.service import  features as featuresDB

class  faceNetLib:
    def __init__(self):
        pass

    def getlib(self):
        known_face_dataset = featuresDB.getFeature()
        return known_face_dataset
