# coding=utf-8
"""
   @author: wy
   @time: 2018/5/25 0025
"""

from src.storage.mysql_pool import MysqlPool
import MySQLdb
import uuid
import cv2
# 获取MysqlPool对象
pool = MysqlPool()


class Camframe():
    """
    实体,对应Camframe表
    """
    def __init__(self,cam_id,framebytes):
        self.id = str(uuid.uuid1())
        self.cam_id = cam_id
        self.framebytes = framebytes

def insert_camframe(camframe):
    """
    插入原始的帧
    :param camframe:
    :return:
    """
    con = pool.getConnection()
    cus = con.cursor()
    try:
        people_sql = "insert into camframe(id,cam_id,framebytes) values (%s,%s,%s)"
        args = (camframe.id,camframe.cam_id,MySQLdb.Binary(camframe.framebytes))
        cus.execute(people_sql,args)             # 执行SQL语句
        con.commit()  # 如果执行成功就提交事务
    except Exception as e:
        con.rollback()                 # 如果执行失败就回滚事务
        raise e
    finally:
        cus.close()
        con.close()

if __name__ == '__main__':
    # f = open("11.png","rb")
    # x = f.read()
    # f.close()

    x = cv2.imread("sigma_2.png")

    for i in range(5):
        camframe = Camframe(2,x)
        insert_camframe(camframe)
