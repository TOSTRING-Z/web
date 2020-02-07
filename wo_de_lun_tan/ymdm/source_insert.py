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
class source_tem(base):
    __tablename__ = 'source_tem'
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
for row in session.query(source_tem).all():
    print('title:{0},path0:{1},time:{2}'.format(row.title,len(row.path0.split(',')),len(row.time.split(','))))
    search = session.query(source).filter(source.title == row.title).first()
    if search:
        #search.year = row.year
        #search.time = row.time
        search.tag = row.tag
        #search.make = row.make
        #search.kan_dian = row.kan_dian
        search.type = row.type
        #search.region = row.region
        #search.subtitle = row.subtitle
        search.imgName = row.imgName
        # path0 = row.path0.split(',')
        # ad = 0
        # for i,item in enumerate(path0):
        #     if len(item.split('|')) > 1:
        #         path0[i] = '第{0}集'.format(item)
        #         ad += 1
        #     else:
        #         path0[i] = str(item)+'|'+str(i-ad+1)
        # search.path1 = search.path0
        # search.path0 = ','.join(path0)
        #search.path1 = search.path0
        # search.browse = search.browse
        # search.up_num = search.up_num
        # search.comment = search.comment
        # search.user_id = search.user_id
        print("updata")
        session.commit()
        continue
    # else:
    #     add = source(title=row.title,
    #                  year=row.year,
    #                  time=row.time,
    #                  tag=row.tag,
    #                  make=row.make,
    #                  kan_dian=row.kan_dian,
    #                  type=row.type,
    #                  region=row.region,
    #                  subtitle=row.subtitle,
    #                  imgName=row.imgName,
    #                  path1=row.path1,
    #                  path2=row.path2,
    #                  path0=row.path0,
    #                  browse=0,
    #                  up_num=0,
    #                  comment=0,
    #                  user_id=1
    #                  )
    #     print("insert")
    #     session.add(add)
    #     session.commit()