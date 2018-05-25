# coding=utf-8
"""
   @author: wy
   @time: 2018/5/24 0024
"""
import pymysql
from src.storage.mysql_config import  db_config
from DBUtils.PooledDB import PooledDB


def singleton(cls):
    instances = {}
    def getinstance(*args,**kwargs):
        if cls not in instances:
            instances[cls] = cls(*args,**kwargs)
        return instances[cls]
    return getinstance

@singleton
class MysqlPool:
    """
    mysql连接池
    """
    def __init__(self):
        #Todo 修改读配置文件
        self.pool = PooledDB(pymysql,2,host='192.168.0.245',user='root',passwd='ueface',db='ueface',port=3306,charset="utf8") #5为连接池里的最少连接数


    def getConnection(self):
        """
        获取连接对象,自动提交
        :return:
        """
        return self.pool.connection()



if __name__ == '__main__':
     # 测试单例
     m1 = MysqlPool()
     m2 = MysqlPool()
     print(m1==m2)

     # 测试事务
     con = m1.getConnection()
     cus = con.cursor()                 # 生成游标对象
     try:
        people_sql = "insert into people(name) values ('hello2');"      # 定义要执行的SQL语句1
        cus.execute(people_sql)        # 执行SQL语句
        id = int(cus.lastrowid)        # 获取上一次插入后得到的ID
        people_sql2 = "insert into people(name) values ('%s');" %(str(id))
        cus.execute(people_sql2)
        con.commit()                   # 如果执行成功就提交事务
        #con.rollback()
     except Exception as e:
        con.rollback()                 # 如果执行失败就回滚事务
        raise e
     finally:
        cus.close()
        con.close()
