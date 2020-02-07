#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import js2py
import json
import os
path = '/home/img/'
import re
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func,text,create_engine,MetaData,Table,Column,Integer,CHAR,Text,TIMESTAMP,VARCHAR,DATETIME
from sqlalchemy.ext.declarative import declarative_base
from requests.exceptions import RequestException
engine = create_engine("mysql+pymysql://root:3317rnpn@cdb-q72em9s2.bj.tencentcdb.com:10179/web", echo=False)
#engine = create_engine("mysql+pymysql://root:root@127.0.0.1/web", echo=False)
dbsession = sessionmaker(bind=engine)
session = dbsession()
base = declarative_base()
class source(base):
    __tablename__ = 'source'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    imgName = Column(Text)
if __name__ == '__main__':
    rows = session.query(source).all()
    for row in rows:
        if os.path.isfile('{}{}.{}'.format(path,row.title,row.imgName.split('.')[-1])):
            continue
        response = requests.get(row.imgName)
        if response.status_code == 200:
            try:
                with open('{}{}.{}'.format(path,row.title,row.imgName.split('.')[-1]), "wb") as f:
                    f.write(response.content)
                    print(row.title)
            except Exception as e:
                with open('{}img_err.txt'.format('/home/'), "a+") as f:
                    f.write('{}/n{}'.format(row.title,row.imgName))
                continue
