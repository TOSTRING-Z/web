
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func,text,create_engine,MetaData,Table,Column,Integer,CHAR,Text,TIMESTAMP,VARCHAR,DATETIME
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine("mysql+pymysql://root:3317rnpn@cdb-q72em9s2.bj.tencentcdb.com:10179/source_web_TT", echo=False)
dbsession = sessionmaker(bind=engine)
session = dbsession()
base = declarative_base()
class source_dilidili(base):
    __tablename__ = 'source_dilidili'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    time = Column(Text)
    type = Column(CHAR(50))
    tag = Column(Text)
    kan_dian = Column(Text)
    make = Column(Text)
    sheng_you = Column(Text)
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
    pan = Column(Text)
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
proxies = {'http': '120.236.128.201:8060',
 'https': '120.236.128.201:8060'
 }
# req=requests.get(url,headers=header,proxies=proxies,timeout=5)
# html=req.text
# soup=BeautifulSoup(html,'lxml')
# print(soup.text)

import re
def get_one_page(url):
    try:
        response=requests.get(url,headers=header,proxies=proxies,timeout=5)
        #print(response)
        if response.status_code == 200:
            r=response.text
            #a=r.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(r)[0])
            return r
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
        html = get_one_page('{0}'.format(url))
        if html:
            url_result = innerText.first(html,'var sourceUrl = "(.*?)";','')
            tit = innerText.first(html,"<h2><a href='http://www.dilidili.name/'>嘀哩嘀哩</a> > <a href='.*?'>.*?</a> > (.*?) .*?</h2>", '')
            if tit:
                if url_result:
                    url_arr.append('{0}|{1}'.format(url_result,tit))
                else:
                    url_arr.append('None|{0}'.format(tit))
            else:
                url_arr.append('None|None')
            print(url_arr[-1])
    return ','.join(url_arr)
if __name__ == '__main__':
    #1000
    for t in range(79000,81000):
        url = 'http://www.dilidili.name/watch3/{}/'.format(t)
        print(url)
        html= get_one_page(url)
        if html:
            title = innerText.first(html, '<meta name="keywords" content="(.*?)" />','')
            if title is None:
                continue
            if session.query(source_dilidili).filter(source_dilidili.title == title.strip()).first():
                continue
            pre_page_url = innerText.first(html,"嘀哩嘀哩</a> > <a href='(.*?)'",'')
            if pre_page_url:
                html_show = get_one_page(pre_page_url)
                if html_show:
                    year = innerText.first(html_show, '<b>年代：</b><a href="/anime/(.*?)/"','')
                    region = innerText.first(html_show,'<div class="d_label"><b>地区：</b><a.*?>(.*?)</a></div>','')
                    kan_dian = innerText.first(html_show,'<b>看点：</b>(.*?)</div>','')
                    sheng_you = innerText.first(html_show,'<b>声优：</b><a href=".*?">(.*?)</a>','')
                    make = innerText.first(html_show,'<b>制作：</b><a href=".*?">(.*?)</a>','')
                    subtitle = innerText.first(html_show,'<p><div class="d_label2"><b>简介：</b>(.*?)</div>','')
                    imgName = innerText.first(html_show, '<dt><img src="(.*?)" alt=".*?"/>', '')
                    pan = innerText.first(html_show,'<li class="list_xz">.*?<a href="(.*?)" target="_blank">','')

                    type_html = innerText.first(html_show, '<div class="d_label"><b>标签：</b>(.*?)</div>', '')
                    type = innerText.all(type_html, '<a href=".*?">(.*?)</a>', ',')

                    url_html = innerText.first(html_show, '<div class="swiper-container swiper4">.*?<ul.*?>(.*?)</ul>', '')
                    if url_html is None:
                        continue
                    url_str = innerText.all(url_html,'<a href="(.*?)" target="_blank" target="_self">',',')
                    if url_str is None or year is None:
                        continue
                    path0 = movie_url(url_str)
                    print('({0})title:{1},year:{2},type:[{3}],region:{4}'.format(t,title,year,type,region))
                    search = session.query(source_dilidili).filter(source_dilidili.title == title).first()
                    if search:
                        continue
                    else:
                        add = source_dilidili(title=title.strip(),
                                                year=year[0:4],
                                                time=year,
                                                type=type,
                                                kan_dian=kan_dian,
                                                sheng_you=sheng_you,
                                                make=make,
                                                region=region,
                                                subtitle=subtitle,
                                                imgName=imgName,
                                                path0=path0,
                                                pan=pan,
                                                browse=0,
                                                up_num=0,
                                                comment=0,
                                                user_id=1
                                                )
                        session.add(add)
                        session.commit()
