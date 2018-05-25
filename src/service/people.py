# coding=utf-8
"""
   @author: wy
   @time: 2018/5/23 0023
"""

from src.storage.mysql_pool import MysqlPool
import MySQLdb
import uuid
import cv2
# 获取MysqlPool对象
pool = MysqlPool()


class People():
    def __init__(self,name,frame):
        self.id = str(uuid.uuid1())
        self.name = name
        self.frame = frame



def insert_people(people):
    con = pool.getConnection()
    cus = con.cursor()
    try:
        people_sql = "insert into people(id,name,imagebytes) values (%s,%s,%s)"
        args = (people.id,people.name,MySQLdb.Binary(people.frame))
        cus.execute(people_sql,args)             # 执行SQL语句
        con.commit()  # 如果执行成功就提交事务
    except Exception as e:
        con.rollback()                 # 如果执行失败就回滚事务
        raise e
    finally:
        cus.close()
        con.close()

if __name__ == '__main__':

    im1 = cv2.imread("sigma_2.png")

    #
    # im2 = cv2.imread("11.png")

    # f = open("11.png",'rb')
    # da1 = f.read()
    # f.close()

    # f = open("sigma_2.png", 'rb')
    # da2 = f.read()
    # f.close()



    for i in range(5):
        people = People("sigma_cv2_byteraary",im1)
        insert_people(people)