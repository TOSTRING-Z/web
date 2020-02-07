from flask import Flask,request,render_template,url_for,redirect,session,flash,Response
from functools import wraps
import json
from werkzeug.utils import secure_filename
import os
import requests
from requests.exceptions import RequestException
# from selenium import webdriver
import re
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
def get_one_page(url):
    response=requests.get(url)
    if response.status_code == 200:
        r = response.text
        try:
            #print(requests.utils.get_encodings_from_content(r)[0])
            if requests.utils.get_encodings_from_content(r)[0] == 'gb2312':
                a=r.encode('ISO-8859-1').decode('gb18030')
            else:
                a = r.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(r)[0])
            return a
        except:
            return r
    return None
class innerText:
    def first(html_in,pattern,split_sel):
        result = re.search(r'{0}'.format(str(pattern)), str(html_in), re.DOTALL)
        if result:
            result_groups = result.groups()
            return split_sel.join(result_groups)
        return None
    def all(html_in,pattern,split_sel):
        result = re.findall(r'{0}'.format(str(pattern)), str(html_in), re.DOTALL)
        if result:
            return split_sel.join(result)
        return None
type_all = {}

def movie_url(url_arr):
    path_ab = 'https://www.55cc.cc/'
    path_all = ['', '', '','']
    for i,urlstr in enumerate(url_arr):
        urls = innerText.all(urlstr,'<a href="(.*?)" class="btn btn-default btn-sm">.*?</a>',',').split(',')
        nums = innerText.all(urlstr,'<a href=".*?" class="btn btn-default btn-sm">(.*?)</a>',',').split(',')
        row = []
        for ii,url in enumerate(urls):
            try:
                path_url = innerText.first(get_one_page(path_ab + url),'<script src="(/5cplay/player.php?.*?)">','')
                path = innerText.first(get_one_page(path_ab + path_url),'src="https:.*?url=(.*?)"','')
                type = 'm3u8'
                if path is None:
                    type = 'html'
                    path = innerText.first(get_one_page(path_ab + path_url), 'src="(.*?)"', '')
                row.append('{}|{}|{}'.format(path,type,nums[ii]))
                print('{} is ok!'.format(url))
            except:
                print(url)
                continue
        path_all[i] = '@@'.join(row)
    return path_all

if __name__ == '__main__':
    #4589
    for t in [35194]:
        url = 'https://www.55cc.cc/dongman/{}/'.format(t)
        html_show = get_one_page(url)
        if html_show:
            title = innerText.first(html_show,'<h4><a href="/dongman/.*?/" class="ff-text">(.*?)</a></h4>','')
            if title:
                search = session.query(source).filter(source.title == title.strip()).first()
                if search:
                    url_arr = innerText.all(html_show,'<ul class="list-unstyled-play text-center play-list">(.*?)</ul>',',').split(',')
                    path = movie_url(url_arr)
                    print(path)
                    try:
                        for item in path:
                            if search.path0 in ['','0','None',None]:
                                search.path0 = item
                                print("updata0")
                            elif search.path1 in ['','0','None',None]:
                                search.path1 = item
                                print("updata1")
                            elif search.path2 in ['','0','None',None]:
                                search.path2 = item
                                print("updata2")
                            elif search.path3 in ['','0','None',None]:
                                search.path3 = item
                                print("updata3")
                            elif search.path4 in ['','0','None',None]:
                                search.path4 = item
                                print("updata4")
                            elif search.path5 in ['','0','None',None]:
                                search.path5 = item
                                print("updata5")
                            session.commit()
                    except:
                        session.rollback()
