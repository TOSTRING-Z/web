import js2py
import os
import requests
from requests.exceptions import RequestException
import re
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func,text,create_engine,MetaData,Table,Column,Integer,CHAR,Text,TIMESTAMP,VARCHAR,DATETIME
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine("mysql+pymysql://root:3317rnpn@cdb-q72em9s2.bj.tencentcdb.com:10179/source_web_TT",echo=False,pool_size=10000)
dbsession = sessionmaker(bind=engine)
base = declarative_base()
session = dbsession()
class source(base):
    __tablename__ = 'source_qqdm'
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
path = '/install/web/wo_de_lun_tan/TT/qqdm/js'
with open(f'{path}/jm.js','r',encoding= 'utf8') as jm:
    str_decode = js2py.eval_js(jm.read())
    def get_one_page(url):
        try:
            response=requests.get(url)
            if response.status_code == 200:
                r=response.text
                a=r.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(r)[0])
                return a
            return None
        except:
            return r
    class innerText:
        def first(html_in,pattern,split_sel):
            result = re.search(r'{0}'.format(pattern), str(html_in), re.DOTALL)
            if result:
                result_groups = result.groups()
                return split_sel.join(result_groups)
            return None
        def all(html_in,pattern,split_sel):
            result = re.findall(r'{0}'.format(pattern), str(html_in), re.DOTALL)
            if result:
                return split_sel.join(result)
            return None
    def movie_url(url_str):
        url_list_arr = []
        for url_list in url_str.split(','):
            u = innerText.all(url_list, '<a href="(.*?)" title=".*?">.*?</a>', ',')
            if u == None:
                continue
            u = u.split(',')
            url_list_arr.append(u)
        tit_list_arr = []
        for tit_list in url_str.split(','):
            t = innerText.all(tit_list, 'href=".*?_(.*?).html"', ',')
            if t == None:
                continue
            t = t.split(',')
            tit_list_arr.append(t)
        path = [0, 0, 0, 0, 0]
        for i,url_list in enumerate(url_list_arr):
            url_arr = []
            for ii,url in enumerate(url_list):
                html = get_one_page('http://www.qiqidongman.com/{}'.format(url))
                if html:
                    url_result = innerText.first(html,'str_decode\("(.*?)"\)','')
                    tit = tit_list_arr[i][ii]
                    if tit and url_result:
                        url_arr.append('{0}|{1}'.format(str_decode(url_result).replace("#", "|"),tit))
                    print(url_arr[-1])
            path[i] = '@@'.join(url_arr)
        return path

    if __name__ == '__main__':
            for t in range(322, 1000):
                url = 'http://www.qiqidongman.com/v/{0}/'.format(t)
                print(t)
                html_show = get_one_page(url)
                if html_show:
                    title = innerText.first(html_show, '<h1>(.*?)</h1>', '')
                    if title:
                        year = innerText.first(html_show,'(\d+?\-\d+?\-\d+?)','')
                        type_html = innerText.first(html_show, '<p class="tags">标签(.*?)</p>', '')
                        type = innerText.all(type_html, '<a.*?>(.*?)</a>', ',')
                        region = innerText.first(html_show,'"/vod-search-area-(.*?).html"','')
                        subtitle = innerText.first(html_show, '<div class="pDesc">.*?<p>(.*?)</p>', '')
                        imgName = innerText.first(html_show,'<div class="DESC-img"><img src="(.*?)".*?>','')
                        url_str = innerText.all(html_show, '<div class="tb fix">(.*?)</div>', ',')
                        if url_str is None or year is None:
                            continue
                        path = movie_url(url_str)
                        print('({})title:{},year:{},type:[{}],region:{}'.format(t,title, year, type, region))
                        #session = dbsession()
                        try:
                            search = session.query(source).filter(source.title == title).first()
                            if search:
                                if search.path0 == path[0]:
                                    search.path0 = path[0]
                                if search.path1 == path[1]:
                                    search.path1 = path[1]
                                if search.path2 == path[2]:
                                    search.path2 = path[2]
                                session.commit()
                                session.close()
                                print('updata')
                            else:
                                add = source(title=title,
                                         year=year.split('-')[0],
                                         time=year,
                                         type=type,
                                         region=region,
                                         subtitle=subtitle,
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
                                session.close()
                        except:
                            session.rollback()
                            with open('err.txt','a') as f:
                                f.write ('{}'.format(t))
                            