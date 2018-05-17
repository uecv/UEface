from    .align_custom import AlignCustom
from  .face_feature import FaceFeature
from  .mtcnn_detect import MTCNNDetect
from  .tf_graph import FaceRecGraph
import cv2
import json
import numpy as np

import  sys

FRGraph = FaceRecGraph();
aligner = AlignCustom();
extract_feature = FaceFeature(FRGraph,model_path="./Model//faceNet/models/model-20170512-110547.ckpt-250000")
face_detect = MTCNNDetect(FRGraph, model_path="./Model/faceNet/models/",scale_factor=2);  # scale_factor, rescales image for faster detection





def  face_locations_encoding(image):
    '''

    :param image:
    :param locations:  list类型，一系列人脸的位置
    :return: 输出人脸的位置，编码，姿态
    '''

    rects, landmarks = face_detect.detect_face(image, 80);  # min face size is set to 80x80
    aligns = []
    positions = []
    for (i, rect) in enumerate(rects):
        aligned_face, face_pos = aligner.align(160, image, landmarks[i])
        if len(aligned_face) == 160 and len(aligned_face[0]) == 160:
            aligns.append(aligned_face)
            positions.append(face_pos)
        else:
            print("Align face failed")  # log

    features_arr=[]
    if (len(aligns) > 0):
        features_arr = extract_feature.get_features(aligns)

    # rects (x,y,w,h) to (x1,y1,x2,y2)

    locations =[]
    for (i,rect) in enumerate(rects):
        xmin = rect[0]
        ymax = rect[1]
        xmax = rect[0]+rect[2]
        ymin = rect[1]+rect[3]

        locations.append([ymin,xmin,ymax,xmax])

        cv2.rectangle(image, (xmin,ymax), (xmax,ymin), (255, 0, 0))





    return np.array(locations),features_arr,positions,image




            # recog_data = findPeople(features_arr, positions);
            # for (i, rect) in enumerate(rects):
            #     cv2.rectangle(image, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]),
            #                   (255, 0, 0))  # draw bounding box for the face




'''
facerec_128D.txt Data Structure:
{
"Person ID": {
    "Center": [[128D vector]],
    "Left": [[128D vector]],
    "Right": [[128D Vector]]
    }
}
This function basically does a simple linear search for 
^the 128D vector with the min distance to the 128D vector of the face on screen
'''
def findPeople(features_arr, positions, data_set=None,thres = 0.6, percent_thres = 85):
    '''
    :param features_arr: a list of 128d Features of all faces on screen
    :param positions: a list of face position types of all faces on screen
    :param thres: d
    istance threshold
    :return: person name and percentage
    '''
    if data_set is None:
        f = open('./facerec_128D.txt','r')
        data_set = json.loads(f.read())
    returnRes = [];
    for (i,features_128D) in enumerate(features_arr):
        result = "Unknown";
        smallest = sys.maxsize
        for person in data_set.keys():
            person_data = data_set[person][positions[i]];
            for data in person_data:
                distance = np.sqrt(np.sum(np.square(data-features_128D)))
                if(distance < smallest):
                    smallest = distance;
                    result = person;
        percentage =  min(100, 100 * thres / smallest)
        if percentage <= percent_thres :
            result = "Unknown"
        returnRes.append((result,percentage))
    return returnRes