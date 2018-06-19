# coding=utf-8
"""
   @author: wy
   @time: 2018/5/23 0023
"""
import uuid
from sqlalchemy import Column, String,DATETIME
import datetime
from src.storage import db
session = db.Session()

class People(db.Base):
    __tablename__ = 'people'
    __table_args__ = {'extend_existing':True}
    """
    实体类,对应数据库中people表
    """
    id = Column(String(36),default=uuid.uuid1(), primary_key=True)
    name = Column(String(20),nullable=False)
    worker_id = Column(String(20))
    image_path = Column(String(100),nullable=False)
    create_time = Column(DATETIME,default=datetime.datetime.utcnow)

    def __repr__(self):
        return "People(%s,%s,%s,%s)" %(str(self.id),self.name,self.worker_id,self.image_path)

def insert_people(people):
    """
    插入人脸信息
    :param people:
    :return:
    """
    session.add(people)
    session.commit()



def get_peoples():
    """
    返回人脸信息
    :return:
    """
    return session.query(People).all()


def get_people(uuid):
    """
    返回人脸信息
    :return:
    """
    return session.query(People(uuid=uuid)).fist()


if __name__ == '__main__':
    p = People(name = 'qwe',image_path = 'dsfsd')
    session.add(p)
    session.commit()
    print(get_peoples())
    our_user = session.query(People).filter_by(name='qwe').first()
    print(our_user)
