from sqlalchemy.orm import sessionmaker
from sqlalchemy import func,text,create_engine,MetaData,Table,Column,Integer,CHAR,Text,TIMESTAMP,VARCHAR,DATETIME
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine("mysql+pymysql://root:3317rnpn@cdb-q72em9s2.bj.tencentcdb.com:10179/web", echo=False)
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
    up_num = Column(Integer)
    comment = Column(Integer)
    imgName = Column(Text)
    subtitle = Column(Text)
    browse = Column(Integer)
    year = Column(Integer)
    region = Column(CHAR(50))
search = session.query(source).all()
for i,item in enumerate(search):
    try:
        # tag_arr = []
        # for tag in item.tag.split(','):
        #     if tag != '':
        #         tag_arr.append(tag)
        #     else:
        #         print(item.tag)
        # item.tag = ','.join(tag_arr)
        type_arr = []
        for type in item.type.split(','):
            if type == '暂无':
                type = '其它'
            if type == '其他':
                type = '其它'
            if type == '校园搞笑':
                type = '校园,搞笑'
            if type == '高笑':
                type = '搞笑'
            if type == '4368':
                type = 'OVA'
            if type == '萝莉':
                type = 'LOLI'
            if type != '':
                type_arr.append(type)
            else:
                print(item.type)
        item.type = ','.join(type_arr)
    except:
        continue
session.commit()