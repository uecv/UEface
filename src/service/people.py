# coding=utf-8
"""
   @author: wy
   @time: 2018/5/23 0023
"""
import uuid
from sqlalchemy import Column, String,DATETIME
from sqlalchemy import UniqueConstraint
import datetime
from sqlalchemy.dialects.postgresql import UUID

from src.storage import db
session = db.Session()

class People(db.Base):
    __tablename__ = 'people'
    __table_args__ = {'extend_existing':True}
    """
    实体类,对应数据库中people表
    """

    id = Column(UUID, primary_key=True,default=uuid)
    name = Column(String(20),nullable=False)
    company_id = Column(String(20),nullable=False)
    worker_id = Column(String(20),nullable=False)
    image_path = Column(String(100),nullable=False)
    create_time = Column(DATETIME,default=datetime.datetime.utcnow)
    UniqueConstraint('name', 'company_id','worker_id', name='uix_people')

    def __repr__(self):
        return "People(%s,%s,%s,%s,%s)" %(str(self.id),self.name,self.company_id,self.worker_id,self.image_path)

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

    for i in range(5):
        uuid = str(uuid.uuid1())
        p = People(name = 'qwe',worker_id='sdsfsdf',company_id="ue",image_path = 'dsfsd',id=uuid)
        session.add(p)
        session.flush()
    # print(get_peoples())
    # our_user = session.query(People).filter_by(name='qwe').first()
    # print(our_user)
