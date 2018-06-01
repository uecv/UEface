
'''用于训练人脸验证模式

模型结构使用CNN的结构。

输入： 2个人脸特征 [2,128]

输入:  相同：1   不相同：0
'''


from sklearn.ensemble import  RandomForestClassifier
import os
from src.FaceDetection.MTCNNDetection import MTCNNDetection
from src.FaceFeature.FaceNet.FaceNetExtract import FaceNetExtract
from src.Config.Config import Config
import  cv2

class RandomForest():
    def __init__(self,data,label):
        self.data = data
        self.label = label


    def  train(self,data):
        '''用于训练随机森林模型'''


        model = RandomForestClassifier(class_weight='balanced', max_features=3, n_estimators=10, min_samples_split=2)
        model.fit(self.data, self.label)

        return model


class  LFW():
    def __init__(self,root,faceDetect, faceFeature):
        self.root = root
        self.parispath= root+"pairs.txt"
        self.faceDetect = faceDetect
        self.faceFeature =faceFeature


    # 读取LFW的pairs.txt保存到result中
    # result是列表，paris是字典，字典元素flag，img1，img2，num1，num2
    def _read_paris(self,filelist="pairs.txt"):
        filelist = str(filelist)
        fp = open(filelist, 'r')
        result = []
        for lines in fp.readlines():
            lines = lines.replace("\n", "").split("\t")
            if len(lines) == 2:
                print("lenth=2:" + str(lines))
                continue
            elif len(lines) == 3:
                pairs = {
                    'flag': 1,
                    'img1': lines[0],
                    'img2': lines[0],
                    'num1': lines[1],
                    'num2': lines[2],
                }
                result.append(pairs)
                continue
            elif len(lines) == 4:
                pairs = {
                    'flag': 2,
                    'img1': lines[0],
                    'num1': lines[1],
                    'img2': lines[2],
                    'num2': lines[3],
                }
                result.append(pairs)
            else:
                print("read file Error!")
                exit()
        fp.close
        print("Read paris.txt DONE!")
        return result


    def _getFaceFeature(self,imagePath):

        frame = cv2.imread(imagePath)
        # locations：人脸位置。  landmarks：人脸特征点
        locations, landmarks = faceDetect.detect(frame)
        # ** 人脸特征抽取
        # features_arr：人脸特征    positions：人脸姿态
        features_arr, positions = faceFeature.Extract(frame, locations, landmarks)
        return features_arr



    def loadFeature_Label(self):
        '''

        :param faceDetect:  人脸检测接口
        :param faceFeature: 人脸特征抽取接口
        :return:
        '''
        pairs = self._read_paris(self.parispath)

        result_X =[]
        result_Y =[]

        for temp in pairs:
            flag = temp['flag']
            img1 = temp['img1']
            img2 = temp['img2']
            num1 = str(temp['num1'].zfill(4))
            num2 = temp['num2'].zfill(4)

            img1name = img1 + "_" + num1 + ".jpg"
            img1path = os.path.join(self.root, img1)
            img1path = os.path.join(img1path, img1name)

            img2name = img2 + "_" + num2 + ".jpg"
            img2path = os.path.join(self.root, img2)
            img2path = os.path.join(img2path, img2name)

            feature1 = self._getFaceFeature(img1path)
            feature2 = self._getFaceFeature(img2path)

            result_X.append([feature1,feature2])
            result_Y.append(flag)

        return (result_X,result_Y)






if __name__ == '__main__':



    '''
    步骤：
    1、读取lfw的pairs.txt文件
    2、根据pairs.txt文件的图片构建特征集合，以及标签集合 【N,2,128】 【N,2】 是否为同一个人
    3、将步骤2的特征输入到随机森林中进行训练
    '''

    # step 1

    lfwRoot = "E:\data\人脸识别\LFW\lfw_funneled\\"

    conf = Config("./Config/config.ini")
    faceDetect = MTCNNDetection(conf)  # 人脸 检测接口
    faceFeature = FaceNetExtract(conf)  # 人脸特征抽取接口
    lfw = LFW(lfwRoot,faceDetect, faceFeature)
    lfw.loadFeature_Label()



    # rf = RandomForest()
    # rf.train()

