# coding=utf-8
"""
   @author: wy
   @time: 2018/5/23 0023
"""
from src.storage.mysql_pool import MysqlPool
# 获取MysqlPool对象
pool = MysqlPool()


def get_nums(cam_id):
    """
    通过摄像头id获取今日已检测人数
    :param cam_id: 摄像头ID
    :return: 返回人数
    """
    db = pool.getConnection()
    cur = db.cursor()
    sql = "select count(*) from recognition t where cam_id = %s and DATE(t.cap_time) = CURRENT_DATE();"
    cur.execute(sql,cam_id)
    res = cur.fetchone()
    count = res[0]
    cur.close()  # or del cur
    db.close()  # or del db
    return count


if __name__ == '__main__':
    print(get_nums(1))


