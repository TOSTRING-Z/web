from flask import Flask,request,render_template,url_for,redirect,session,flash,Response
from functools import wraps
import json
from werkzeug.utils import secure_filename
import os
import requests
import re
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func,text,create_engine,MetaData,Table,Column,Integer,CHAR,Text,TIMESTAMP,VARCHAR,DATETIME
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine("mysql+pymysql://root:root@127.0.0.1/source_web_TT", echo=False)
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

class innerText:
    def first(html_in,pattern,split_sel):
        result = re.search(r'{0}'.format(pattern), html_in, re.DOTALL).groups()
        return split_sel.join(result)
    def all(html_in,pattern,split_sel):
        return split_sel.join(re.findall(r'{0}'.format(pattern), html_in, re.DOTALL))
def movie_url(url_str):
    url_arr = []
    for url in url_str.split(','):
        html = requests.get(url).text
        url_result = innerText.first(html,'<video class="dplayer-video dplayer-video-current".*?src="(.*?)">','')
        url_arr.append(url_result)
        tit = innerText.first(html,'<span>.*?第(.*?)集</span>','')
    return '|{0},'.format(tit).join(url_arr)

for t in range(0,5000):
    url_show = 'http://www.yhdm.tv/show/{0}.html'.format(t)
    html_show = requests.get(url_show).text
    title = innerText.first(html_show,'<h1>(.*?)</h1>')
    time = innerText.first(html_show, '<span><label>上映:</label><a href=".*?" target="_blank">(.*?)</a>-(.*?)-\d+</span>','')
    type_html = innerText.first(html_show, '<label>类型:</label>(.*?)</span>','')
    type = innerText.all(type_html,'<a href=".*?" target="_blank">(.*?)</a>',',')
    region = innerText.first(html_show,'<span><label>地区:</label><a href=".*?" target="_blank">(.*?)</a></span>','')
    subtitle = innerText.first(html_show,'<div class="info">(.*?)</div>','')
    url_html = innerText.first(html_show,'<div class="movurl" style="display:block"><ul>(.*?)</ul></div>','')
    imgName = innerText.first(html_show,'<div class="thumb l"><div class="splay">.*?src="(.*?)" alt=".*?"></div>','')
    url_str = innerText.all(url_html,'<li><a href="(.*?)" target="_blank">第.*?集</a></li>',',')
    path1 = movie_url(url_str)