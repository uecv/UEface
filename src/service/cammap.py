# coding=utf-8
"""
   @author: wy
   @time: 2018/5/25 0025
"""

from src.storage.mysql_pool import MysqlPool
# 获取MysqlPool对象
pool = MysqlPool()


class Cammap:
    """
    实体类,对应数据库中people表
    """
    def __init__(self,name,map_name,image_path):
        self.id = 0
        self.map_name = map_name
        self.image_path = image_path


def get_peoples():
    """
    返回人脸信息
    :return:
    """
    con = pool.getConnection()
    cus = con.cursor()
    result = None
    try:
        sql = "select id,image_path from people"
        cus.execute(sql)             # 执行SQL语句
        result = cus.fetchall()
    except Exception as e:
        con.rollback()                 # 如果执行失败就回滚事务
        raise e
    finally:
        cus.close()
        con.close()
        return result