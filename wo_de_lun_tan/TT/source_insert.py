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
    title = Column(Text)
    path1 = Column(Text)
    path2 = Column(Text)
    path0 = Column(Text)
    path3 = Column(Text)
    path4 = Column(Text)
    path5 = Column(Text)
class source_qqdm(base):
    __tablename__ = 'source_qqdm'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    path0 = Column(Text)
    path1 = Column(Text)
    path2 = Column(Text)
for row in session.query(source_qqdm).all():
    search = session.query(source).filter(source.title == row.title).first()
    if search:
        search.path3 = row.path0
        search.path4 = row.path1
        search.path5 = row.path2
        print("updata")
        session.commit()
    else:
        print('{}:fail'.format(row.title))