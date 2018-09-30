# coding=utf-8
import uuid
from sqlalchemy import Column,String,DATETIME,Integer,cast,DATE,func
from sqlalchemy import UniqueConstraint
import datetime
from src.storage import db


session = db.Session()



class Recoginition(db.Base):
    __tablename__ = 'recognition'
    __table_args__ = {'extend_existing':True}


    """
    实体类，对应数据库中recognition表
    """
    # Todo id自增
    id = Column(Integer,autoincrement=True,primary_key=True)
    cam_id = Column(Integer,nullable=False)
    user_id = Column(Integer,nullable=False)
    cap_time = Column(DATETIME,default=datetime.datetime)

    def __repr__(self):
        return "Recogintion(%s,%s,%s,%s)"%(str(self.id),self.cam_id,self.user_id,self.cap_time)


def get_today_nums(today):
    date = datetime.datetime.strptime(today,"%Y-%m-%d")
    print ('date',date)
    know_id = session.query(Recoginition).filter(cast(Recoginition.cap_time, DATE)==date,Recoginition.user_id !="Unknown").count()
    unknow_id = session.query(Recoginition).filter(cast(Recoginition.cap_time, DATE)==date,Recoginition.user_id =="Unknown").count()
    return dict({'know':know_id,
            'unknow':unknow_id,
            'total':know_id+unknow_id})

def get_last_week(today):
    date = datetime.datetime.strptime(today,"%Y-%m-%d")
    know_id = session.query(func.date_format(Recoginition.cap_time, "%Y-%m-%d"),func.count()).filter(Recoginition.user_id !="Unknown").group_by(cast(Recoginition.cap_time,DATE)).all()
    unknow_id = session.query(func.date_format(Recoginition.cap_time, "%Y-%m-%d"),func.count()).filter(Recoginition.user_id =="Unknown").group_by(cast(Recoginition.cap_time,DATE)).all()
    print ('know_id',know_id)
    print ('unknow_id',unknow_id)
    week_list = [(datetime.datetime.today()-datetime.timedelta(i)).strftime("%Y-%m-%d")for i in range(0,7)]
    unknow_week_dict = {i:0 for i in week_list}
    know_week_dict = {i:0 for i in week_list}
    #Todo 推导式化
    for i in unknow_id:
        if i[0] in unknow_week_dict.keys():
            unknow_week_dict[i[0]] = i[1]
    for i in know_id:
        if i[0] in know_week_dict:
            know_week_dict[i[0]] = i[1]
    return dict({'know':know_week_dict,
                 'unknow':unknow_week_dict})




def insert_result(recogn):
    session.add(recogn)
    session.commit()

if __name__ == '__main__':
    # recon = Recoginition(cam_id=1,user_id=1,cap_time=datetime.datetime.now())
    # session.add(recon)
    # session.commit()
    # insert_result(recon)
    # print(get_nums(1))
    print (get_last_week('2018-09-29'))

"""
#建表sql
create table recognition
(
id int primary key NOT NULL AUTO_INCREMENT comment 'uuid,主键',
cam_id int not null comment  '外键,摄像头ID',
user_id varchar(128) not null comment '外键,该头像识别得到的人id',
cap_time DATETIME not null comment '被捕捉到的时间',
create_time DATETIME DEFAULT CURRENT_TIMESTAMP  comment '创建时间',
description VARCHAR(100)  comment '备注'
) comment='识别结果表'

"""
"""
#写入数据库
                    if id == "Unknown":
                        recongize_result = recoginiton.Recoginition(img_head_str, 1, 1, id, time)
                        recoginiton.insert_result(recongize_result)
                        continue
                    recongize_result = recoginiton.Recoginition(img_head_str,1,1,id,time)
                    recoginiton.insert_result(recongize_result)

"""
# """
#    @author: wy
#    @time: 2018/5/23 0023
# """
# import uuid
# from src.storage.mysql_pool import MysqlPool
# import MySQLdb
# import datetime
# import  cv2
# # 获取MysqlPool对象
# pool = MysqlPool()
#
# class Recoginition():
#     def __init__(self,cap_img,cam_id,frame_id,user_id,cap_time):
#         """
#         :param cap_img: 从帧中扣出的头像
#         :param cam_id: 外键,摄像头ID
#         :param frame_id: 外建,所属帧ID
#         :param user_id: 外键,该头像识别得到的人id
#         :param cap_time: 被捕捉到的时间
#         """
#         self.id = str(uuid.uuid1())
#         self.cap_img = cap_img
#         self.cam_id = cam_id
#         self.frame_id = frame_id
#         self.user_id = user_id
#         self.cap_time = cap_time
#
# def get_nums(cam_id):
#     """
#     通过摄像头id获取今日已检测人数
#     :param cam_id: 摄像头ID
#     :return: 返回人数
#     """
#     db = pool.getConnection()
#     cur = db.cursor()
#     sql = "select count(*) from recognition t where cam_id = %s and DATE(t.cap_time) = CURRENT_DATE();"
#     cur.execute(sql,cam_id)
#     res = cur.fetchone()
#     count = res[0]
#     cur.close()  # or del cur
#     db.close()  # or del db
#     return count
#
# def insert_result(reco):
#     con = pool.getConnection()
#     cus = con.cursor()
#     try:
#         sql = "insert into recognition(id,cap_img,cam_id,frame_id,user_id,cap_time) values (%s,%s,%s,%s,%s,%s)"
#         args = (reco.id,
#                 MySQLdb.Binary(reco.cap_img),
#                 reco.cam_id,
#                 reco.frame_id,
#                 reco.user_id,
#                 reco.cap_time)
#         cus.execute(sql,args)             # 执行SQL语句
#         con.commit()  # 如果执行成功就提交事务
#     except Exception as e:
#         con.rollback()                 # 如果执行失败就回滚事务
#         raise e
#     finally:
#         cus.close()
#         con.close()
#
# if __name__ == '__main__':
#     # 获取今日统计人数测试
#     print(get_nums(1))
#     # # 测试写入识别结果
#     # f = open("11.png","rb")
#     # x = f.read()
#     # f.close()
#     x = cv2.imread("sigma_2.png")
#     dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     for i in range(5):
#         reco = Recoginition(x,1,1,1,dt)
#         insert_result(reco)
#
#
