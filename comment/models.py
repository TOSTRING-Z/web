import functools
import re

from sqlalchemy.orm import sessionmaker
from sqlalchemy import exists,func,not_,text,create_engine,MetaData,Table,Column,Integer,CHAR,Text,TIMESTAMP,VARCHAR,DATETIME
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/blogs", echo=False)
dbsession = sessionmaker(bind=engine)
base = declarative_base()

class article(base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True)
    time = Column(TIMESTAMP)
    content = Column(Text)
    tag = Column(Text)
    title = Column(Text)
    img = Column(Text)
    subtitle = Column(Text)
class comment(base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    content = Column(Text)
    time = Column(TIMESTAMP)
    article_id = Column(Integer)
    comment_num = Column(Integer)
class comment_response(base):
    __tablename__ = 'comment_response'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    target_user_id = Column(Integer)
    content = Column(Text)
    time = Column(TIMESTAMP)
    comment_id = Column(Integer)
class user(base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    user_name = Column(VARCHAR)
    email = Column(Text)
    web_site = Column(Text)

def mException(func):
    @functools.wraps(func)
    def wrapper(session=dbsession(),*args,**kwargs):
        try:
            return func(session,*args,**kwargs)
        except Exception as e:
            print(e)
            session.rollback()
            session.close()
            return None
        finally:
            session.close()
    return wrapper

@mException
def getUser(session=dbsession(),*args,**kwargs):
    return session.query(user).filter(user.id == kwargs['id']).first()
@mException
def mainRead(session=dbsession(),*args,**kwargs):
    result = session.query(article).order_by(article.time.asc()).limit(5).offset(kwargs['index']).all()
    arr = []
    for d in result:
        d.subtitle = re.sub('(<img.*?>.*?</.*?>|<iframe.*?>.*?</.*?>|<video.*?>.*?</.*?>|<.*?>)', '',d.subtitle)
        d.subtitle = (d.subtitle[0:70] + '[...]') if len(d.subtitle) > 69 else d.subtitle
        arr.append({
            'id':d.id,
            'subtitle':d.subtitle,
            'title':d.title,
            'img':d.img,
            'tag':d.tag,
            'time':d.time.strftime('%Y-%m-%d')
        })
    lens = session.query(func.count('*')).select_from(article).scalar()
    data = {'len': lens, 'data': arr}
    return data
@mException
def detailRead(session=dbsession(),*args,**kwargs):
    result = session.query(article).filter(article.id == kwargs['id']).first()
    data = {
            'id':result.id,
            'subtitle':result.subtitle,
            'title':result.title,
            'img':result.img,
            'tag':result.tag,
            'content': result.content,
            'time':result.time.strftime('%Y-%m-%d')
        }
    return data
@mException
def tagRead(session=dbsession(),*args,**kwargs):
    result = session.query(article).filter(article.tag == kwargs['tag']).order_by(article.time.asc()).limit(5).offset(kwargs['index']).all()
    arr = []
    for d in result:
        d.subtitle = re.sub('(<img.*?>.*?</.*?>|<iframe.*?>.*?</.*?>|<video.*?>.*?</.*?>|<.*?>)', '',d.subtitle)
        d.subtitle = (d.subtitle[0:70] + '[...]') if len(d.subtitle) > 69 else d.subtitle
        arr.append({
            'id':d.id,
            'subtitle':d.subtitle,
            'title':d.title,
            'img':d.img,
            'tag':d.tag,
            'time':d.time.strftime('%Y-%m-%d')
        })
    lens = session.query(func.count('*')).select_from(article).filter(article.tag == kwargs['tag']).scalar()
    data = {'len': lens, 'data': arr}
    return data
@mException
def tagClassRead(session=dbsession(),*args,**kwargs):
    nums = func.count('*').label('c')
    result = session.query(article.tag, nums).group_by(article.tag).all()
    data = []
    for d in result:
        data.append({
                'tag':d[0],
                'num': d[1]
            })
    return data
@mException
def commentIdRead(session=dbsession(),*args,**kwargs):
    result = session.query(comment).filter(comment.article_id == kwargs['id']).all()
    data = []
    for d in result:
        user_info = getUser(id=d.user_id)
        data.append({
            'user': user_info.user_name,
            'time': d.time.strftime('%Y-%m-%d'),
            'content': d.content.replace('&[','<img style="width:20px" src="/static/public/OwO/aLu/').replace(']&','.png">'),
            'comment_num': d.comment_num or 0,
            'detail_id':d.id,
            })
    return data

@mException
def commenHuifuRead(session=dbsession(),*args,**kwargs):
    result = session.query(comment_response).filter(comment_response.comment_id == kwargs['detail_id']).all()
    data = []
    for d in result:
        user_info = getUser(id=d.user_id)
        target_user_info = getUser(id=d.target_user_id)
        data.append({
            'user': user_info.user_name,
            'time': d.time.strftime('%Y-%m-%d'),
            'content': d.content.replace('&[','<img style="width:20px" src="/static/public/OwO/aLu/').replace(']&','.png">'),
            'detail_id': d.comment_id,
            'target_user_id': d.target_user_id,
            'target_user_name': target_user_info.user_name
        })
    return data
@mException
def owoSubmitRead(session=dbsession(),*args,**kwargs):
    user_info = session.query(user).filter(user.email == kwargs['email']).first()
    if user_info:
        if user_info.user_name != kwargs['user_name'] or user_info.web_site != kwargs['web_site']:
            user_info.user_name = kwargs['user_name']
            user_info.web_site = kwargs['web_site']
        session.flush()
        if kwargs['type'] == 'comment':
            add_item = comment(user_id=int(user_info.id), content=kwargs['content'], article_id=int(kwargs['detail_id']), comment_num=0)
            session.add(add_item)
        if kwargs['type'] == 'comment_response':
            updata = session.query(comment).filter(comment.id == kwargs['detail_id']).first()
            updata.comment_num = updata.comment_num + 1
            add_item = comment_response(user_id=int(user_info.id), content=kwargs['content'], comment_id=int(kwargs['detail_id']), target_user_id=int(kwargs['target_user_id']))
            session.add(add_item)
    else:
        user_new = user(user_name=kwargs['user_name'], email=kwargs['email'], web_site=kwargs['web_site'])
        session.add(user_new)
        session.flush()
        if kwargs['type'] == 'comment':
            add_item = comment(user_id=int(user_new.id), content=kwargs['content'], article_id=int(kwargs['detail_id']),comment_num=0)
            session.add(add_item)
        if kwargs['type'] == 'comment_response':
            updata = session.query(comment).filter(comment.id == kwargs['detail_id']).first()
            updata.comment_num = updata.comment_num + 1
            add_item = comment_response(user_id=int(user_new.id), content=kwargs['content'], comment_id=int(kwargs['detail_id']), target_user_id=int(kwargs['target_user_id']))
            session.add(add_item)
    session.commit()
