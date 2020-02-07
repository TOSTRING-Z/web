#!/install/python3
from urllib import parse,request
from bs4 import BeautifulSoup
import re
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from flask import Flask,request,render_template,url_for,redirect,session,flash,Response
from functools import wraps
import json
from werkzeug.utils import secure_filename
import os
import requests
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func,text,create_engine,MetaData,Table,Column,Integer,CHAR,Text,TIMESTAMP,VARCHAR,DATETIME
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine("mysql+pymysql://root:3317rnpn@cdb-q72em9s2.bj.tencentcdb.com:10179/web", echo=False)
#engine = create_engine("mysql+pymysql://root:root@127.0.0.1/web", echo=False)
dbsession = sessionmaker(bind=engine)
session = dbsession()
base = declarative_base()
class source(base):
    __tablename__ = 'source'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    time = Column(Text)
    type = Column(CHAR(50))
    tag = Column(Text)
    title = Column(Text)
    path1 = Column(Text)
    path2 = Column(Text)
    path0 = Column(Text)
    up_num = Column(Integer)
    comment = Column(Integer)
    imgName = Column(Text)
    subtitle = Column(Text)
    browse = Column(Integer)
    year = Column(Integer)
    region = Column(CHAR(50))

def inline(doc):
    return '''data:text/html;charset=utf-8,'''.format(parse.quote(doc))

if __name__ == '__main__':
    search = session.query(source)[2385:]
    for i, item in enumerate(search):
        # print(item.path0)
        # item.path0 = item.path0.replace('&amp;','&')
        #print(item.path0)
        # session.commit()
        # continue
        if item.path0 is None:
            continue
        url_arr = []
        for ii,url in enumerate(item.path0.split(',')):
            if url.split('|')[0].isdigit():
                print(item.title+'(id:'+str(item.id)+'):'+str(ii))
                display = Display(visible=0, size=(800, 600))
                display.start()

                driver = webdriver.Firefox()
                driver.get('http://106.53.77.53:8081/mv?param='+parse.quote('https://api.jialingmm.net/mmletv/mms.php?type=letv&vid={}'.format(url.split('|')[0])))
                try:
                    driver.implicitly_wait(0)
                    #iframe = driver.find_element_by_tag_name('iframe')
                    iframe = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "iframe"))
                    )
                finally:
                    driver.switch_to.frame(iframe)
                    try:
                        try:
                            video = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.ID, "videoPlayer"))
                            )
                        except:
                            url_arr.append(url)
                            driver.quit()
                    finally:
                        try:
                            text = BeautifulSoup(driver.page_source)
                            miPlayer = text.find('div', id='player')
                            url_re = miPlayer.find('video').get('src')
                            print(url)
                            url_arr.append(url_re+'|'+url.split('|')[1])
                            print(url_arr[-1])
                            driver.quit()
                            display.stop()
                        except:
                            url_arr.append(parse.unquote(url))
                            driver.quit()
            else:
                url_arr.append(url)
        item.path0 = ','.join(url_arr)
        session.commit()
        #print(url_arr)
        print('------------------------------------------------------------')