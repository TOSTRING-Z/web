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
# engine = create_engine("mysql+pymysql://root:root@127.0.0.1/web", echo=False)
dbsession = sessionmaker(bind=engine)
session = dbsession()
base = declarative_base()
class source(base):
    __tablename__ = 'source'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    time = Column(Text)
    type = Column(CHAR(50))
    make = Column(CHAR(50))
    kan_dian = Column(Text)
    tag = Column(Text)
    title = Column(Text)
    path1 = Column(Text)
    path2 = Column(Text)
    path0 = Column(Text)
    path3 = Column(Text)
    path4 = Column(Text)
    path5 = Column(Text)
    up_num = Column(Integer)
    comment = Column(Integer)
    imgName = Column(Text)
    subtitle = Column(Text)
    browse = Column(Integer)
    year = Column(Integer)
    region = Column(CHAR(50))
    other_name = Column(Text)
def movie_url(url_str):
    path_all = [None, None, None,None,None, None]
    html = get_one_page('http://m.imomoe.io{0}'.format(url_str.split(',')[0]))
    if html:
        script_url = innerText.first(html,'<script type="text/javascript" src="(.*?)">','')
        script_result = get_one_page('http://m.imomoe.io{0}'.format(script_url))
        url_arr_all = script_result.split('],[')
        for index,item in enumerate(url_arr_all):
            url_arr = []
            url_result_re = innerText.all(item, '\'\\\\u.*?\\\\u.*?\$(.*?)\$.*?\'', '$')
            tit_re = innerText.all(item, '\'(\\\\u.*?\\\\u.*?)\$.*?\$.*?\'', '$')
            type_re = innerText.all(item, '\'\\\\u.*?\\\\u.*?\$.*?\$(.*?)\'', '$')
            if tit_re and url_result_re:
                url_result = url_result_re.split('$')
                type = type_re.split('$')
                tit = tit_re.split('$')
                for i, url_result_item in enumerate(url_result):
                    if i < len(tit):
                        url_arr.append('{0}|{1}|{2}'.format(url_result_item, type[i], tit[i]))
            else:
                continue
            path_all[index] = '@@'.join(url_arr)
            print(url_arr)
    return path_all

def get_one_page(url):
    try:
        response=requests.get(url)
        if response.status_code == 200:
            r=response.text
            #print(requests.utils.get_encodings_from_content(r)[0])
            if requests.utils.get_encodings_from_content(r)[0] == 'gb2312':
                a=r.encode('ISO-8859-1').decode('gb18030')
            else:
                a = r.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(r)[0])
            return a
        return None
    except:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
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

def updata(t):
    url = 'http://m.imomoe.io/view/{0}.html'.format(t)
    html_show = get_one_page(url)
    if html_show:
        title = innerText.first(html_show, '<h1 class="am-header-title">(.*?)</h1>', '')
        if title:
            year = innerText.first(html_show, '<i class="am-icon-clock-o"></i><a.*?>(.*?)</a>', '')
            other_name = innerText.first(html_show, '<p><i class="am-icon-info-circle"></i>(.*?)</p>', '')
            type_html = innerText.first(html_show, '<i class="am-icon-tag"></i>(.*?)</p>', '')
            type = innerText.all(type_html, str('<a.*?>(.*?)</a>'), ',')
            region = innerText.first(html_show, '<i class="am-icon-location-arrow"></i><a.*?>(.*?)</a>', '')
            imgName = innerText.first(html_show, 'class="am-intro-left am-u-sm-5"><img src="(.*?)".*?/>', '')
            subtitle = innerText.first(html_show, '<p class="txtDesc autoHeight">(.*?)</p>', '')
            url_html = innerText.first(html_show, '<ul class="mvlist">(.*?)</ul>', '')
            if url_html is None or year is None or title is None or type is None or region is None or subtitle is None:
                return None
            path = (movie_url(innerText.all(url_html, '<a.*?href=\'(.*?)\' target="_blank">', ',')))
            print('title:{0},year:{1},type:[{2}],region:{3}'.format(title.strip(), year, type, region))
            search = session.query(source).filter(source.title == title.strip()).first()
            if search:
                try:
                    if len(path[0].split('@@')) == len(path[1].split('@@')):
                        search.path0 = path[1]
                        search.path1 = path[0]
                    else:
                        search.path0 = path[0]
                        search.path1 = path[1]
                    search.other_name = other_name
                    for item in path:
                        if item in ['', '0', 'None', None]:
                            continue
                        print(search.path0)
                        if search.path0 in ['', '0', 'None', None,item] or 'm.imomoe.net' in search.path0:
                            search.path0 = item
                            print("updata0")
                        elif search.path1 in ['', '0', 'None', None,item]:
                            search.path1 = item
                            print("updata1")
                        elif search.path2 in ['', '0', 'None', None,item]:
                            search.path2 = item
                            print("updata2")
                        elif search.path3 in ['', '0', 'None', None,item]:
                            search.path3 = item
                            print("updata3")
                        elif search.path4 in ['', '0', 'None', None,item]:
                            search.path4 = item
                            print("updata4")
                        elif search.path5 in ['', '0', 'None', None,item]:
                            search.path5 = item
                            print("updata5")
                        # with open('/install/web/source_web_TT/time.txt', 'a') as f:
                        #     f.write('{}:{}'.format(title.strip(),search.path0.split('@@')[-1].split('|')[-1]))
                    session.commit()
                    session.close()
                    return None
                except:
                    session.rollback()
                    return None
            else:
                add = source(title=title.strip(),
                             year=year.strip(),
                             time='',
                             type=type.strip(),
                             region=region.strip(),
                             subtitle=subtitle.strip(),
                             imgName=imgName,
                             path0=path[0],
                             path1=path[1],
                             path2=path[2],
                             browse=0,
                             up_num=0,
                             comment=0,
                             user_id=1,
                             other_name=other_name
                             )
                session.add(add)
                session.commit()

url = 'http://m.imomoe.io/'
html_show = get_one_page(url)
# search = session.query(source).filter(text('FIND_IN_SET("新番连载",tag)')).all()
# for item in search:
#     all_tag = []
#     for tag in item.tag.split(','):
#         if tag != '新番连载' and tag != '':
#             all_tag.append(tag)
#     item.tag = ','.join(all_tag)
#     print(all_tag)
#     print('delect tag:'+item.title)
#     session.commit()
day = [1,2,3,4,5,6,0]
if __name__ == '__main__':
    if html_show:
        all = innerText.all(html_show,'<ul class="am-list">(.*?)</ul>',',').split(',')
        for i,item in enumerate(all):
            all_title = innerText.all(item,'<a.*?>(.*?)</a>',',').split(',')
            id = innerText.all(item,'<a href="/view/(.*?).html".*?">',',').split(',')
            for t in id:
                updata(t)
            # for title in all_title:
            #     search = session.query(source).filter(source.title == title).first()
            #     if search:
            #         search.title = title
            #         if '新番连载' in str(search.tag):
            #             continue
            #         if search.tag is None:
            #             search.tag = '新番连载'
            #         else:
            #             search.tag = '{0},新番连载'.format(search.tag)
            #         search.time = day[i]
            #         print('add tag:'+title)
            #         session.commit()

