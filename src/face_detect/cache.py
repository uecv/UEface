# coding=utf-8
"""
   @author: wy
   @time: 2018/5/29 0029
"""
from src.Config.Config import Config
from utils.redis_queue import RedisQueue
from src.service import people
from PIL import Image
from io import BytesIO
import base64
import os


if __name__ == '__main__':

    conf = Config("./Config/config.ini")
    # 读取数据库人脸数据
    result = people.get_peoples()

    # 以人的ID为key,图片的base64编码存到redis中
    q = RedisQueue('rq',host="192.168.0.245")
    for id,image_path in result:
        im = Image.open(os.path.join(conf.get("cache","imagepath"),image_path))
        buffered = BytesIO()
        im.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        q.set(id,img_str)
