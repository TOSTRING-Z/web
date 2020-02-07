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
    other_name = Column(Text)
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
type_all = {}
def movie_url(t,url_str):
    path_all = [None, None, None,None]
    html = get_one_page('http://m.imomoe.io{0}'.format(url_str.split(',')[0]))
    if html:
        script_url = innerText.first(html,'<script type="text/javascript" src="(.*?)">','')
        script_result = get_one_page('http://m.imomoe.io{0}'.format(script_url))
        url_arr_all = script_result.split('],[')
        for index,item in enumerate(url_arr_all):
            url_arr = []
            url_result_re = innerText.all(item,'\'\\\\u.*?\\\\u.*?\$(.*?)\$.*?\'','$')
            tit_re = innerText.all(item,'\'(\\\\u.*?\\\\u.*?)\$.*?\$.*?\'','$')
            type_re = innerText.all(item,'\'\\\\u.*?\\\\u.*?\$.*?\$(.*?)\'','$')
            if tit_re and url_result_re:
                url_result = url_result_re.split('$')
                type = type_re.split('$')
                tit = tit_re.split('$')
                for i,url_result_item in enumerate(url_result):
                    if type[i] not in type_all:
                        type_all[type[i]] = t
                        print(type[i])
                    if i < len(tit):
                        url_arr.append('{0}|{1}|{2}'.format(url_result_item,type[i],tit[i]))
            else:
                continue
            path_all[index] = '@@'.join(url_arr)
            print(url_arr)
    return path_all

if __name__ == '__main__':
    #4589
    yhid = []
    for t in range(7574,7575):
        url = 'http://m.imomoe.io/view/{0}.html'.format(t)

        html_show = get_one_page(url)
        if html_show:
            title = innerText.first(html_show,'<h1 class="am-header-title">(.*?)</h1>','')
            if title:
                year = innerText.first(html_show, '<i class="am-icon-clock-o"></i><a.*?>(.*?)</a>','')
                other_name = innerText.first(html_show, '<p><i class="am-icon-info-circle"></i>(.*?)</p>','')
                type_html = innerText.first(html_show, '<i class="am-icon-tag"></i>(.*?)</p>','')
                type = innerText.all(type_html,str('<a.*?>(.*?)</a>'),',')
                region = innerText.first(html_show,'<i class="am-icon-location-arrow"></i><a.*?>(.*?)</a>','')
                imgName = innerText.first(html_show, 'class="am-intro-left am-u-sm-5"><img src="(.*?)".*?/>', '')
                subtitle = innerText.first(html_show,'<p class="txtDesc autoHeight">(.*?)</p>','')
                url_html = innerText.first(html_show,'<ul class="mvlist">(.*?)</ul>','')
                if url_html is None or year is None or title is None or type is None or region is None or subtitle is None:
                    continue
                path = (movie_url(t,innerText.all(url_html,'<a.*?href=\'(.*?)\' target="_blank">',',')))
                print('title:{0},year:{1},type:[{2}],region:{3}'.format(title.strip(),year,type,region))
                search = session.query(source).filter(source.title == title.strip()).first()
                if search:
                    try:
                        search.other_name = other_name
                        #search.imgName = imgName
                        # if 'vod.300hu.com' in path[0]:
                        #     search.path0 = path[0]
                        #     yhid.append(t)

                        if search.path0 != path[0]:
                            search.path0 = path[0]
                            print("updata0")
                        if search.path1 != path[1]:
                            search.path1 = path[1]
                            print("updata1")
                        if search.path2 != path[2]:
                            search.path2 = path[2]
                            print("updata2")
                        session.commit()
                        continue
                    except:
                        session.rollback()
                        continue
                else:
                    add = source(title=title.strip(),
                                 year=year.strip(),
                                 time=year.strip(),
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
                                 user_id=1
                                 )
                    session.add(add)
                    session.commit()
    with open('/home/yh_300hu_id','w+') as f:
        f.write(json.dumps(yhid))
