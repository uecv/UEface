# coding=utf-8

import uuid
from sqlalchemy import Column, String,DATETIME,Integer
from sqlalchemy.dialects.mysql import  LONGTEXT
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
import  base64
import datetime
import  pandas as pd
import numpy as np
from src.storage import db
session = db.Session()

class Feature(db.Base):
    __tablename__ = 'feature'
    __table_args__ = {'extend_existing': True}

    """
       实体类。
       """

    id = Column(Integer,autoincrement=True, primary_key=True)

    people_id = Column(String(36))

    feature = Column(LONGTEXT)

    def __repr__(self):
        return "People(%s,%s,%s)" %(str(self.id),self.people_id,self.feature)


def insert_feature(feature):
    """
    插入人脸信息
    :param people:
    :return:
    """
    session.add(feature)
    session.commit()


def getFeature():
    featuredf = pd.read_sql('feature',db.engine).infer_objects()
    QueryDist = dict(zip(featuredf['people_id'],featuredf['feature']))
    result= {}
    for key in QueryDist:
        strs = QueryDist[key]
        basess  = base64.b64decode(strs)
        value = np.fromstring(basess,dtype=np.float32)
        result[key]=value


    return result


if __name__ == '__main__':
    # f =  Feature(people_id="",feature=""
    # session.add(f)
    # session.commit()

    Featuredf = getFeature()

    for temp in Featuredf:

        print("success")

    print("success")