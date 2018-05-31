#coding:utf-8

import unittest
from src.FaceDetection.MTCNNDetection import MTCNNDetection
from PIL import Image

class MTCNNTest(unittest.TestCase):
    def test_mtcnn(self):
        mtcnn = MTCNNDetection()
        image = Image.open('/home/kenwood/图片/钢鑫_12.jpg','r')
        print (image)
        print(mtcnn.detect(image))

