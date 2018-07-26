# coding=utf-8
"""
   @author: wy
   @time: 2018/5/23 0023
"""
import uuid
from sqlalchemy import Column, String,DATETIME
from sqlalchemy import UniqueConstraint
import datetime
from src.storage import db
session = db.Session()


def generate_uuid():
    return str(uuid.uuid1())

class People(db.Base):
    __tablename__ = 'people'
    __table_args__ = {'extend_existing':True}
    """
    实体类,对应数据库中people表
    """
    id = Column(String(36), primary_key=True)
    name = Column(String(55),nullable=False)
    company_id = Column(String(55),nullable=False)
    worker_id = Column(String(55),nullable=False)
    image_path = Column(String(100),nullable=False)
    create_time = Column(DATETIME,default=datetime.datetime.utcnow)
    UniqueConstraint(name, company_id,worker_id, name='uix_people')

    def __repr__(self):
        return "People(%s,%s,%s,%s,%s)" %(str(self.id),self.name,self.company_id,self.worker_id,self.image_path)

def insert_people(people):
    """
    插入人脸信息
    :param people:
    :return:
    """
    people.id = generate_uuid()
    session.add(people)
    session.commit()



def getfilterPeople(people):

    result = session.query(People).filter(People.worker_id==people.worker_id)\
        .filter(People.company_id==people.company_id)\
        .filter(People.name ==people.name).all()

    return result


def get_peoples():
    """
    返回所有人脸信息
    :return:
    """
    return session.query(People).all()


def get_people(uuid):
    """
    返回人脸信息
    :return:
    """
    return session.query(People).filter(People.id==uuid).first()


if __name__ == '__main__':

    # 测试循环插入
    # for i in range(0,3):
    #     p = People(name = u'伊任华',worker_id=u'011',company_id=u'useease',image_path =  u'伊任华-011.jpg')
    #
    #     ss = getfilterPeople(p)
    #     print("success")
    #     # insert_people(p)

    # # 查询所有数据
    print(get_people('c4ba49f8-746d-11e8-8e8d-88d7f69262f6'))
    # # 查询个别数据
    # our_user = session.query(People).filter_by(name='qwe').first()
    # print(our_user)