# coding=utf-8
"""
   @author: wy
   @time: 2018/5/25 0025
"""

from src.storage.mysql_pool import MysqlPool
import MySQLdb
# 获取MysqlPool对象
pool = MysqlPool()

class Camera():
    def __init__(self,cam_name,map_id,url,x,y):
        self.cam_name = cam_name
        self.map_id = map_id
        self.url = url
        self.x=x
        self.y=y

def insert_camera(camera):
    """
    增加摄像头
    :param camera:
    :return:
    """
    con = pool.getConnection()
    cus = con.cursor()
    try:
        people_sql = "insert into camera(cam_name,map_id,url,x,y) values (%s,%s,'%s',%s,%s)"
        args = (camera.cam_name,camera.map_id,camera.url,camera.x,camera.y)
        cus.execute(people_sql,args)             # 执行SQL语句
        con.commit()  # 如果执行成功就提交事务
    except Exception as e:
        con.rollback()                 # 如果执行失败就回滚事务
        raise e
    finally:
        cus.close()
        con.close()

def get_cameras():
    con = pool.getConnection()
    cus = con.cursor()
    result = None
    try:
        sql = "select id,cam_name,map_id,url,x,y from cameras"
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
    camera = Camera("摄像头A",)
    insert_camera()
    #print(get_cameras())