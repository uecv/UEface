# coding=utf-8
"""
   @author: wy
   @time: 2018/5/29 0029
"""
from utils.redis_queue import RedisQueue
from src.storage.mysql_pool import MysqlPool

if __name__ == '__main__':
    # 获取数据库连接
    db = MysqlPool()
    conn = db.getConnection()

    result = None
    # 读取数据库人脸数据
    with conn.cursor() as cursor:
        # Read a single record
        sql = "select t.id,t.image_path from people t"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
    conn.close

    # 以人的ID为key,图片的base64编码存到redis中
    q = RedisQueue('rq')
    for id,image_path in result:
        im = Image.open(image_path)
        buffered = BytesIO()
        im.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        q.set(id,img_str)
