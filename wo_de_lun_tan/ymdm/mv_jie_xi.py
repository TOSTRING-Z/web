#新浪
#http://ask.ivideo.sina.com.cn/v_play_ipad.php?vid=120107814&uid=1&pid=1&tid=334&plid=4001&prid=ja_7_2184731619&referrer=http%3A%2F%2Fvideo.sina.com.cn&ran=0.16339&r=video.sina.com.cn&v=4.1.43.10&&p=i&k=c25d39e5ba5a48f1
import requests
from urllib import parse
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
header = {
'Host': parse.quote('api.xiaomingming.org'),
'User-Agent':parse.quote('Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'),
'Accept': parse.quote('text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
'Accept-Language': parse.quote('zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'),
'Accept-Encoding': parse.quote('gzip, deflate, br'),
'Cookie': parse.quote('UM_distinctid=16cf5594a72449-0649633ba1f78a-396b4645-1fa400-16cf5594a7435b; CNZZDATA1261531716=73060751-1567484300-null%7C1567911270'),
'Connection': parse.quote('keep-alive'),
'Upgrade-Insecure-Requests':parse.quote('1'),
}
header_xmm = {
'Host': parse.quote('ask.ivideo.sina.com.cn'),
'User-Agent': parse.quote('Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'),
'Accept': parse.quote('text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
'Accept-Language': parse.quote('zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'),
'Accept-Encoding': parse.quote('gzip, deflate'),
'Cookie': parse.quote('SINAGLOBAL=113.5.6.87_1566818553.526629; U_TRS1=0000001b.3e284ac4.5d713112.2513a57e; UOR=cn.bing.com,blog.sina.com.cn,; ULV=1567868281244:2:2:2:113.5.7.9_1567868279.354399:1567699218708; co=113.5.7.9_1567823014.614; SUB=_2AkMqLz_5f8NxqwJRmP4XzWjlbIpwyAvEieKcc84iJRMyHRl-yD9jqh0FtRB6Aa8RFnNnqK3r7DT52P94IeKhk0ahujL1; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFoGGkDbcorO6ulQamdUVlB; SGUID=1567868279534_56119642; UM_distinctid=16d0c3b674d1ad-0deefbcc8175b9-396b4645-1fa400-16d0c3b674f4c4; lxlrttp=1560672234; JAVAVIDEO=f5e52db3b2b79d09a364648b85e8ec67'),
'Connection': parse.quote('keep-alive'),
'Upgrade-Insecure-Requests': parse.quote('1')
}
proxies = {'http': '120.236.128.201:8060',
           'https': '120.236.128.201:8060'
           }
search = session.query(source)[275:]
for i, item in enumerate(search):
    if item.path1 is None:
        continue
    url_arr = []
    for ii,url in enumerate(item.path1.split('@@')):
        if url.split('|')[1] == :
            url_res = 'https://api.xiaomingming.org/cloud/sina.php?vid={}'.format(url.split('|')[0])
            response=requests.get(url_res,headers=header)
            if response.status_code == 200:
                try:
                    url_res_t = innerText.first(response.text,r'video =  \'(.*?)\'','')
                    res = requests.get(url_res_t,allow_redirects=False)
                    #reditList = res.history
                    #print(res.headers["location"])
                    url_arr.append('{0}|{1}'.format(res.headers["location"],url.split('|')[1]))
                    print(str(item.id)+'|'+item.title+'|'+str(url.split('|')[1])+'|'+res.headers["location"])
                except:
                    url_arr.append(url)
                    continue
            url_arr.append(url)
    if url_arr != []:
        item.path1 = ','.join(url_arr)
        print(url_arr)
        #session.commit()