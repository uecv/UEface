
'''
用于在图片中添加水印
'''
import cv2

from PIL import  Image,ImageDraw,ImageFont
import  numpy as np
import os

from skimage import io, transform










def build(path):
    '''
    读取path路径，将该路径下的所有图片数据，添加水印后，存放在Watermarkimage文件夹中
    :param path:
    :return:
    '''

    dirList = os.listdir(path)
    count = 0
    for  file in dirList:
        imagePath = os.path.join(path,file)
        isdir = os.path.isdir(imagePath)
        if(not  isdir): #如果不是目录
            im = cv2.imdecode(np.fromfile(imagePath, dtype=np.uint8), -1)
            sp = im.shape
            center_height = int(sp[1] / 2)
            center_wide = int(sp[0] / 2)
            cv2_rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            pil_im = Image.fromarray(cv2_rgb)
            pil_im = pil_im.rotate(45, expand=1)
            draw = ImageDraw.Draw(pil_im)
            font = ImageFont.truetype("simhei.ttf", 10, encoding="utf-8")
            draw.text((0, center_height), "只用于优亿科技人脸识别项目，只用于优亿科技人脸识别项目，只用于优亿科技人脸识别项目，只用于优亿科技人脸识别项目", (160, 160, 160), font=font)
            pil_im = pil_im.rotate(-45, expand=0)

            after = pil_im.size

            left = int((after[0]-sp[0])/2)

            upper = int((after[1]-sp[1])/2)

            right = int(left + sp[0])

            lower = int(upper+sp[1])

            box = (left,lower,right, upper)
            # pil_im = pil_im.crop(box)


            cv2_tex_im = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)

            writePath =os.path.join("WatermarkImage/",imagePath)

            cv2.imwrite(writePath,cv2_tex_im)

            count+=1
            print(count)





if __name__ == '__main__':
    build("images/lfw/")