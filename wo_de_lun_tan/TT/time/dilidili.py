import js2py
import os
import requests
from requests.exceptions import RequestException
import re
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func,text,create_engine,MetaData,Table,Column,Integer,CHAR,Text,TIMESTAMP,VARCHAR,DATETIME
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine("mysql+pymysql://root:3317rnpn@cdb-q72em9s2.bj.tencentcdb.com:10179/web",echo=False,pool_size=10000)
dbsession = sessionmaker(bind=engine)
base = declarative_base()
session = dbsession()
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
if __name__ == '__main__':
    url = 'http://www.dilidili.name/'
    html_show = get_one_page(url)
    days = [1, 2, 3, 4, 5, 6, 0]
    if html_show:
        time_all = innerText.first(html_show, '<div class="change">\s{0,}<div class="sldr">(.*?)<div class="clear"></div>', '')
        time_arr = innerText.all(time_all,'<li class=".*?">(.*?)<!--.*?end -->',',').split(',')
        search = session.query(source).filter(text('FIND_IN_SET("新番连载",tag)')).all()
        for item in search:
            all_tag = []
            for tag in item.tag.split(','):
                if tag.strip() != '新番连载' and tag.strip() != '' and tag.strip() != 'None':
                    all_tag.append(tag.strip())
            item.tag = ','.join(all_tag)
            print(all_tag)
            print('delect tag:' + item.title)
            session.commit()
        for time,val in enumerate(time_arr):
            day = innerText.all(val,'<a href=".*?/">(.*?)</a>',',').split(',')
            for title in day:
                try:
                    search = session.query(source).filter(source.title.like('%{}%'.format(title))).first()
                    if search:
                        search.time = days[time]
                        if search.tag != '':
                            search.tag = '{},新番连载'.format(search.tag)
                        else:
                            search.tag = '新番连载'.format(search.tag)
                        session.commit()
                        session.close()
                        print(f'updata_{title}_{days[time]}')
                except:
                    session.rollback()