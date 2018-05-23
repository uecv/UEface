
import  json
class  faceNetLib:
    def __init__(self,conf):
        self._path = conf.get("path","faceLibPath")



    def getlib(self):
        f = open(self._path, 'r')
        known_face_dataset = json.loads(f.read())  # 人脸特征库
        f.close()

        return known_face_dataset