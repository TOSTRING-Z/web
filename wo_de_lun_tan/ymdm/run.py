from flask import Flask,request,render_template,url_for,redirect,session,flash,Response
from functools import wraps
import json
from werkzeug.utils import secure_filename
import os
import requests
from requests.exceptions import RequestException
import re
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func,text,create_engine,MetaData,Table,Column,Integer,CHAR,Text,TIMESTAMP,VARCHAR,DATETIME
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine("mysql+pymysql://root:3317rnpn@cdb-q72em9s2.bj.tencentcdb.com:10179/source_web_TT", echo=False)
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
    try:
        response=requests.get(url)
        if response.status_code == 200:
            r=response.text
            a=r.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(r)[0])
            return a
        return None
    except RequestException:
        return None
class innerText:
    def first(html_in,pattern,split_sel):
        result = re.search(r'{0}'.format(pattern), html_in, re.DOTALL)
        if result:
            result_groups = result.groups()
            return split_sel.join(result_groups)
        return None
    def all(html_in,pattern,split_sel):
        result = re.findall(r'{0}'.format(pattern), html_in, re.DOTALL)
        if result:
            return split_sel.join(result)
        return None
def movie_url(url_str):
    url_arr = []
    for url in url_str.split(','):
        html = get_one_page('http://www.yhdm.tv{0}'.format(url))
        if html:
            url_result = innerText.first(html,'onClick="changeplay\(\'(.*?)\$.*?\'\);">','')
            tit = innerText.first(html, '<span>.*?第(.*?)集</span>', '')
            if tit:
                if url_result:
                    url_arr.append('{0}|{1}'.format(url_result,tit))
                else:
                    url_arr.append('None|{0}'.format(tit))
            else:
                url_arr.append('None|None')
            print(url_arr[-1])
    return '@@'.join(url_arr)

if __name__ == '__main__':
    #1000
    for t in range(1000,1500):
        url = 'http://www.yhdm.tv/show/{0}.html'.format(t)
        html_show = get_one_page(url)
        if html_show:
            title = innerText.first(html_show,'<h1>(.*?)</h1>','')
            if title:
                year = innerText.first(html_show, '<span><label>上映:</label><a href=".*?" target="_blank">(.*?)</a>-(.*?)-\d+</span>','')
                type_html = innerText.first(html_show, '<label>类型:</label>(.*?)</span>','')
                type = innerText.all(type_html,'<a href=".*?" target="_blank">(.*?)</a>',',')
                region = innerText.first(html_show,'<span><label>地区:</label><a href=".*?" target="_blank">(.*?)</a></span>','')
                subtitle = innerText.first(html_show,'<div class="info">(.*?)</div>','')
                url_html = innerText.first(html_show,'<div class="movurl".*?><ul>(.*?)</ul></div>','')
                if url_html is None:
                    continue
                imgName = innerText.first(html_show,'<div class="thumb l"><div class="splay">.*?src="(.*?)" alt=".*?"></div>','')
                url_str = innerText.all(url_html,'<li><a href="(.*?)".*?第.*?集</a></li>',',')
                if url_str is None or year is None:
                    continue
                path1 = movie_url(url_str)
                print('title:{0},year:{1},type:[{2}],region:{3}'.format(title,year,type,region))
                search = session.query(source).filter(source.title == title).first()
                if search:
                    continue
                else:
                    add = source(title=title,
                                 year=year,
                                 time=year,
                                 type=type,
                                 region=region,
                                 subtitle=subtitle,
                                 imgName=imgName,
                                 path1=path1,
                                 browse=0,
                                 up_num=0,
                                 comment=0,
                                 user_id=1
                                 )
                    session.add(add)
                    session.commit()
