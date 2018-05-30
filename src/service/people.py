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
    def __init__(self,name,iamge_path):
        self.id = str(uuid.uuid1())
        self.name = name
        self.iamge_path = iamge_path


def insert_people(people):
    con = pool.getConnection()
    cus = con.cursor()
    try:
        people_sql = "insert into people(id,name,iamge_path) values (%s,%s,%s)"
        args = (people.id,people.name,people.iamge_path)
        cus.execute(people_sql,args)             # 执行SQL语句
        con.commit()  # 如果执行成功就提交事务
    except Exception as e:
        con.rollback()                 # 如果执行失败就回滚事务
        raise e
    finally:
        cus.close()
        #con.close()

if __name__ == '__main__':
    f = open("11.png","rb")
    x = f.read()
    f.close()
    people = People("test",x)
    insert_people(people)