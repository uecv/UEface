# coding=utf-8
"""
   @author: wy
   @time: 2018/5/23 0023
"""

from src.storage.mysql_pool import MysqlPool
import MySQLdb
# 获取MysqlPool对象
pool = MysqlPool()


class People():
    def __init__(self,name,frame):
        self.name = name
        self.frame = frame



def insert_people(people):
    con = pool.getConnection()
    cus = con.cursor()
    try:
        people_sql = "insert into people(name,imagebytes) values (%s,%s)"
        args = (people.name,MySQLdb.Binary(people.frame))
        cus.execute(people_sql,args)             # 执行SQL语句
        con.commit()  # 如果执行成功就提交事务
    except Exception as e:
        con.rollback()                 # 如果执行失败就回滚事务
        raise e
    finally:
        cus.close()
        con.close()

if __name__ == '__main__':
    f = open("11.png","rb")
    x = f.read()
    insert_people("test",x)