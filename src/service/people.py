# coding=utf-8
"""
   @author: wy
   @time: 2018/5/23 0023
"""

from src.storage.mysql_pool import MysqlPool
import uuid
# 获取MysqlPool对象
pool = MysqlPool()


class People():
    """
    实体类,对应数据库中people表
    """
    def __init__(self,name,image_path):
        self.id = str(uuid.uuid1())
        self.name = name
        self.image_path = image_path


def insert_people(people):
    """
    插入人脸信息
    :param people:
    :return:
    """
    con = pool.getConnection()
    cus = con.cursor()
    try:
        people_sql = "insert into people(id,name,image_path) values (%s,%s,%s)"
        args = (people.id,people.name,people.image_path)
        cus.execute(people_sql,args)             # 执行SQL语句
        con.commit()  # 如果执行成功就提交事务
    except Exception as e:
        con.rollback()                 # 如果执行失败就回滚事务
        raise e
    finally:
        cus.close()
        con.close()

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


if __name__ == '__main__':
    people = People("test","11.png")
    insert_people(people)
    result = get_peoples()
    print(result)