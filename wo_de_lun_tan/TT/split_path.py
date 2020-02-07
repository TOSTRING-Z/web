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
class innerText:
    def first(html_in,pattern):
        result = re.search(r'{0}'.format(str(pattern)), str(html_in), re.DOTALL)
        if result:
            result_groups = result.groups()
            return result_groups
        return None
    def all(html_in,pattern):
        result = re.findall(r'{0}'.format(str(pattern)), str(html_in), re.DOTALL)
        if result:
            return result
        return None
if __name__ == '__main__':
    data = session.query(source)[:]
    for row in data:
        res = []
        path2 = row.path2
        if path2:
            if '@@' in path2:
                continue
            path = '{},'.format(path2)
            path_url = innerText.all(path,r'(.*?)\|.*?\|\\u.*?\\u.*?,')
            path_type = innerText.all(path, r'.*?\|(.*?)\|\\u.*?\\u.*?,')
            path_name = innerText.all(path, r'.*?\|.*?\|(\\u.*?\\u.*?),')
            for i,item in enumerate(path_url):
                res.append('{}|{}|{}'.format(path_url[i],path_type[i],path_name[i]))
            row.path2 = '@@'.join(res)
            print(row.id)
            session.commit()