from py.mysql_conn import *
import os
import time
import random
import json
import operator
import py.mysql_conn as connect
import re
conn = connect.conn().obj_conn()
color = {
    0:'#bfbfbf',
    1:'#84b0f1',
    2:'#ffc028',
    3:'#95be3e',
    4:'#f2604f',
    5:'#ff9101'
}
UPLOAD_FOLDER = '/install/web/wo_de_lun_tan'
#用户表
class user(conn.base):
    __tablename__ = 'user'
    id = Column(Integer,primary_key = True)
    user_name = Column(CHAR(50))
    age = Column(Integer)
    sex = Column(Integer)
    birthday = Column(CHAR(50))
    phone = Column(CHAR(50))
    email = Column(CHAR(50))
    hobbies = Column(CHAR(50))
    net_name = Column(CHAR(50))
    sersonal_signature = Column(Text)
    registration_time = Column(TIMESTAMP)
    Landing_time = Column(TIMESTAMP)
    address = Column(CHAR(50))
    account = Column(CHAR(50))
    password = Column(CHAR(50))
    vip = Column(Integer)
    balance = Column(Integer)
    experence = Column(Integer)
#板块
class plate(conn.base):
    __tablename__ = 'plate'
    id = Column(Integer, primary_key=True)
    plate_name = Column(CHAR(50))
    subplate_name = Column(CHAR(50))
    subplate_master_id = Column(Integer)
    time = Column(TIMESTAMP)
#classification
class classification(conn.base):
    __tablename__ = 'classification'
    id = Column(Integer, primary_key=True)
    plate_id = Column(Integer)
    type = Column(CHAR(50))
    type_name = Column(CHAR(50))
#主表
class main(conn.base):
    __tablename__ = 'main'
    plate_id = Column(Integer)
    title_id = Column(Integer, primary_key=True)
    up_id = Column(Integer)
    creation_time = Column(TIMESTAMP)
    type = Column(CHAR(50))
    title = Column(CHAR(50))
    subtitle = Column(Text)
    up_num = Column(Integer)
    down_num = Column(Integer)
    comment = Column(Integer)
    imgName = Column(Text)

#细节表
class detail(conn.base):
    __tablename__ = 'detail'
    id = Column(Integer, primary_key=True)
    title_id = Column(Integer)
    message_user_id = Column(Integer)
    up_num = Column(Integer)
    down_num = Column(Integer)
    message_time = Column(TIMESTAMP)
    message_content = Column(Text)
    comment = Column(Integer)
    message_up_id = Column(Integer)
    imgName = Column(Text)

#回复表
class comment(conn.base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    target_user_id = Column(Integer)
    target_title_id = Column(Integer)
    detail_id = Column(Integer)
    time = Column(TIMESTAMP)
    content = Column(Text)

#files
class files(conn.base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    name = Column(CHAR(50))
    type = Column(Text)

#关注表user_follow
class user_follow(conn.base):
    __tablename__ = 'user_follow'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    follow_id = Column(Integer)
    time = Column(TIMESTAMP)

#收藏表user_collection_name
class user_collection(conn.base):
    __tablename__ = 'user_collection'
    id = Column(Integer, primary_key=True)
    title_id = Column(Integer)
    user_id = Column(Integer)
    title_name = Column(CHAR(50))
    time = Column(TIMESTAMP)

#message_response
class message_response(conn.base):
    __tablename__ = 'message_response'
    id = Column(Integer, primary_key=True)
    response_id = Column(Integer)
    user_id = Column(Integer)
    title_id = Column(Integer)
    content = Column(Text)
    time = Column(TIMESTAMP)
    detail_id = Column(Integer)
    comment_id = Column(Integer)


#message_follow
class message_follow(conn.base):
    __tablename__ = 'message_follow'
    id = Column(Integer, primary_key=True)
    follow_id = Column(Integer)
    user_id = Column(Integer)
    time = Column(TIMESTAMP)

#message_leaving
class message_leaving(conn.base):
    __tablename__ = 'message_leaving'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    target_id = Column(Integer)
    content = Column(Text)
    time = Column(TIMESTAMP)

#leaving_message
class leaving_message(conn.base):
    __tablename__ = 'leaving_message'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    target_id = Column(Integer)
    content = Column(Text)
    time = Column(TIMESTAMP)

#tem_upload
class tem_upload(conn.base):
    __tablename__ = 'tem_upload'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
########################################################################################################################
#资源
class source(conn.base):
    __tablename__ = 'source'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    time = Column(Text)
    type = Column(CHAR(50))
    tag = Column(Text)
    title = Column(Text)
    path0 = Column(Text)
    path1 = Column(Text)
    path2 = Column(Text)
    path3 = Column(Text)
    path4 = Column(Text)
    path5 = Column(Text)
    up_num = Column(Integer)
    comment = Column(Integer)
    imgName = Column(Text)
    subtitle = Column(Text)
    browse = Column(Integer)
    year = Column(Integer)
#资源detail
class source_detail(conn.base):
    __tablename__ = 'source_detail'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    source_id = Column(Integer)
    time = Column(TIMESTAMP)
    content = Column(Text)
    up_num = Column(Integer)
    comment = Column(Integer)
#回复表
class source_comment(conn.base):
    __tablename__ = 'source_comment'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    target_user_id = Column(Integer)
    target_source_id = Column(Integer)
    detail_id = Column(Integer)
    time = Column(TIMESTAMP)
    content = Column(Text)
#source_response
class source_response(conn.base):
    __tablename__ = 'source_response'
    id = Column(Integer, primary_key=True)
    response_id = Column(Integer)
    user_id = Column(Integer)
    source_id = Column(Integer)
    content = Column(Text)
    time = Column(TIMESTAMP)
    detail_id = Column(Integer)
    comment_id = Column(Integer)
#source_love
class source_love(conn.base):
    __tablename__ = 'source_love'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    source_id = Column(Integer)
########################################################################################################################


#登陆验证
def deng_lu_yan_zheng(user_name,password):
    session = conn.dbsession()
    try:
        result_user = session.query(user).filter(user.user_name == user_name).first()
        if result_user:
            if result_user.password == password:
                if result_user.Landing_time.strftime('%Y-%m-%d') != time.strftime("%Y-%m-%d", time.localtime()):
                    result_user.Landing_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    result_user.experence += 10
                    session.commit()
                return session.query(user).filter(user.user_name == user_name).first()
            else:
                return 1
        else:
            return 0
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
#注册验证
def zhu_ce_yan_zheng(user_name,password):
    session = conn.dbsession()
    try:
        result_user = session.query(user).filter(user.user_name == user_name).first()
        if result_user:
            return 0
        else:
            user_this = user(user_name = user_name, password = password,sex = 0,sersonal_signature = '这里什么都没有哦~',balance = 0,vip = 0,experence = 0,Landing_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            session.add(user_this)
            session.commit()
            return user_this
    except:
        session.rollback()
        session.close()
    finally:
        session.close()

#留言发送
def detail_send(title_id,message_user_id,message_content):
    session = conn.dbsession()
    try:
        message = detail(title_id = title_id,message_user_id = message_user_id,message_content = message_content)
        session.add(message)
        session.commit()
        return message
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
#留言读取
def detail_read(title_id):
    session = conn.dbsession()
    try:
        result = session.query(detail).filter(detail.title_id == title_id).all()
        return result
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
#留言删除
def detail_delete(message_user_id,message_time):
    session = conn.dbsession()
    try:
        delete = detail(message_user_id = message_user_id, message_time = message_time)
        session.delete(delete)
        session.commit()
    except:
        session.rollback()
        session.close()
    finally:
        session.close()

#新建讨论
def creat_discuss(plate_id,up_id,type,title,subtitle,imgName):
    session = conn.dbsession()
    try:
        result = main(plate_id = plate_id,up_id = up_id,type = type,title = title,subtitle = subtitle,up_num=0,comment = 0,imgName = imgName)
        session.add(result)
        for name in imgName.split('|'):
            file = session.query(tem_upload).filter(tem_upload.name == name).first()
            if file:
                session.delete(file)
        session.commit()
    except:
        session.rollback()
        session.close()
    finally:
        session.close()

#新建detail
def creat_detail(user_id,up_id,title_id,content,imgName):
    session = conn.dbsession()
    try:
        result = detail(message_user_id=user_id,message_up_id=up_id,title_id=title_id, message_content=content, up_num=0, comment=0,imgName = imgName)
        session.add(result)
        session.flush()
        result_message_response = message_response(detail_id=result.id,user_id=up_id, response_id=user_id, content=content, title_id=title_id)
        session.add(result_message_response)
        updata = session.query(main).filter(main.title_id == title_id).first()
        updata.comment = updata.comment + 1
        for name in imgName.split('|'):
            file = session.query(tem_upload).filter(tem_upload.name == name).first()
            if file:
                session.delete(file)
        session.commit()
    except:
        session.rollback()
        session.close()
    finally:
        session.close()

# 新建comment
def creat_comment(detail_id,user_id,target_user_id,target_title_id,content):
    session = conn.dbsession()
    try:
        result = comment(detail_id = detail_id,user_id = user_id,target_title_id = target_title_id,target_user_id = target_user_id,content = content)
        session.add(result)
        session.flush()
        result_message_response = message_response(detail_id=detail_id,comment_id=result.id,user_id=target_user_id, response_id=user_id, content=content,title_id=target_title_id)
        session.add(result_message_response)
        updata = session.query(detail).filter(detail.id == detail_id).first()
        updata.comment = updata.comment + 1
        session.commit()
    except:
        session.rollback()
        session.close()
    finally:
        session.close()


#新建file
def creat_file(name,type):
    session = conn.dbsession()
    try:
        tem = tem_upload(name = name)
        session.add(tem)
        result = files(name = name,type = type)
        session.add(result)
        session.commit()
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
#论坛读取
def main_read(plate_id,type,search):
    session = conn.dbsession()
    try:
        if plate_id is '':
            result = session.query(main).filter(main.title.like('%{search}%'.format(search=search))).all()
        else:
            if type == 'quan_bu' or type is None:
                if search is None or search == 'None':
                    result = session.query(main).filter(main.plate_id == plate_id).order_by(main.creation_time.desc()).all()
                else:
                    result = session.query(main).filter(main.plate_id == plate_id).filter(main.title.like('%{search}%'.format(search = search))).order_by(main.creation_time.desc()).all()
            else:
                if search is None or search == 'None':
                    result = session.query(main).filter(main.plate_id == plate_id).filter(main.type == type).order_by(main.creation_time.desc()).all()
                else:
                    result = session.query(main).filter(main.plate_id == plate_id).filter(main.type == type).filter(main.title.like('%{search}%'.format(search = search))).order_by(main.creation_time.desc()).all()
        return result
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
#detail_main_read读取
def detail_main_read(title_id):
    session = conn.dbsession()
    try:
        result = session.query(main).filter(main.title_id == title_id).first()
        if result:
            result.up_name = user_name(result.up_id)
            return result
        return ''
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
#detail_read读取
def detail_read(title_id):
    session = conn.dbsession()
    try:
        result = session.query(detail).filter(detail.title_id == title_id).order_by(detail.message_time.desc()).all()
        if result:
            return result
        return ''
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
#plate读取
def plate_read(plate_id):
    session = conn.dbsession()
    try:
        result = session.query(plate).filter(plate.id == plate_id).with_lockmode('read').first()
        if result:
            return result
        return ''
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
# plate读取all
def plate_read_all():
    session = conn.dbsession()
    try:
        result = session.query(plate).all()
        data = {}
        for i,plates in enumerate(result):
            if plates.plate_name in data.keys():
                data[plates.plate_name][i] = plates
            else:
                data[plates.plate_name] = {}
                data[plates.plate_name][i] = plates
        return data
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
#comment读取
def comment_read(detail_id):
    session = conn.dbsession()
    try:
        result = session.query(comment).filter(comment.detail_id == detail_id).all()
        if result:
            return result
        return ''
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
#leaving_message读取
def leaving_message_read(user_id):
    session = conn.dbsession()
    try:
        result = session.query(leaving_message).filter(leaving_message.target_id == user_id).all()
        if result:
            return result
        return ''
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
#种类
def classification_read(plate_id):
    session = conn.dbsession()
    try:
        result = session.query(classification).filter(classification.plate_id == plate_id).all()
        if result:
            return result
        return ''
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
#detail_main点赞
def detail_main_up_down_result(title_id,type):
    session = conn.dbsession()
    try:
        if type == "up":
            updata = session.query(main).filter(main.title_id == title_id).first()
            updata.up_num = updata.up_num + 1
            up_num = updata.up_num
            session.commit()
            return up_num
        else:
            updata = session.query(main).filter(main.title_id == title_id).first()
            updata.up_num = updata.up_num - 1
            up_num = updata.up_num
            session.commit()
            return up_num
    except:
        session.rollback()
        session.close()
    finally:
        session.close()

#新建关注user_follow
def user_follow_creat(user_id,follow_id):
    session = conn.dbsession()
    try:
        result_user = session.query(user_follow).filter(user_follow.user_id == user_id).filter(user_follow.follow_id == follow_id).first()
        result_user_message = session.query(message_follow).filter(message_follow.user_id == follow_id).filter(message_follow.follow_id == user_id).first()
        if result_user:
            if result_user_message:
                session.delete(result_user_message)
            session.delete(result_user)
            session.commit()
            return '取消关注!'
        else:
            result = user_follow(user_id=user_id, follow_id=follow_id)
            result_message_follow = message_follow(user_id=follow_id, follow_id=user_id)
            session.add(result_message_follow)
            session.add(result)
            session.commit()
            return '关注成功!'
    except:
        session.rollback()
        session.close()
    finally:
        session.close()

#新建收藏user_collection
def user_collection_creat(user_id,title_id,title_name):
    session = conn.dbsession()
    try:
        result_user = session.query(user_collection).filter(user_collection.user_id == user_id).filter(user_collection.title_id == title_id).first()
        if result_user:
            session.delete(result_user)
            session.commit()
            return '取消收藏!'
        else:
            result = user_collection(user_id=user_id, title_id=title_id,title_name=title_name)
            session.add(result)
            session.commit()
            return '收藏成功!'
    except:
        session.rollback()
        session.close()
    finally:
        session.close()

#用户信息
def user_read(user_id):
    session = conn.dbsession()
    try:
        user_data =  session.query(user).filter(user.id == user_id).first()
        if user_data:
            user_data.level = int(user_data.experence/1000)
            if user_data.level > 5:
                user_data.level = 5
        else:
            class user_data:
                level = 0
        user_data.color = color[user_data.level]
        return user_data
    except Exception as e:
        print(e)
        session.rollback()
        session.close()
    finally:
        session.close()
def user_title_read(user_id):
    session = conn.dbsession()
    try:
        return session.query(main).filter(main.up_id == user_id).all()
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
def user_detail_read(user_id):
    session = conn.dbsession()
    try:
        return session.query(detail).filter(detail.message_user_id == user_id).all()
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
def user_comment_read(user_id):
    session = conn.dbsession()
    try:
        return session.query(comment).filter(comment.user_id == user_id).all()
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
def user_follow_read(user_id):
    session = conn.dbsession()
    try:
        return session.query(user_follow).filter(user_follow.user_id == user_id).all()
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
def user_collection_read(user_id):
    session = conn.dbsession()
    try:
        return session.query(user_collection).filter(user_collection.user_id == user_id).all()
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
#用户信息修改
def user_information(user_id,name,password,sex,birthday,phone,email,hobbies,sersonal_signature):
    session = conn.dbsession()
    try:
        result_user = session.query(user).filter(user.id == user_id).first()
        result_user.user_name = name
        result_user.password = password
        result_user.sex = sex
        result_user.birthday = birthday
        result_user.phone = phone
        result_user.email = email
        result_user.hobbies = hobbies
        result_user.sersonal_signature = sersonal_signature
        session.commit()
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
#message
def message_read(user_id):
    session = conn.dbsession()
    try:
        message = {
            'response': {},
            'follow': {},
            'leaving': {},
            'sourceResponse':{}
        }
        response = session.query(message_response).filter(message_response.user_id == user_id).all()
        for i,delete_response in enumerate(response):
            message['response'][i] = {}
            message['response'][i]['response_id'] = delete_response.response_id
            message['response'][i]['response_name'] = user_name(delete_response.response_id)
            message['response'][i]['content'] = delete_response.content
            message['response'][i]['title_id'] = delete_response.title_id
            message['response'][i]['time'] = delete_response.time.strftime('%Y-%m-%d')
            session.delete(delete_response)
            session.commit()

        follow = session.query(message_follow).filter(message_follow.user_id == user_id).all()
        for i,delete_follow in enumerate(follow):
            message['follow'][i] = {}
            message['follow'][i]['follow_id'] = delete_follow.follow_id
            message['follow'][i]['follow_name'] = user_name(delete_follow.follow_id)
            message['follow'][i]['time'] = delete_follow.time.strftime('%Y-%m-%d')
            session.delete(delete_follow)
            session.commit()

        leaving = session.query(message_leaving).filter(message_leaving.target_id == user_id).all()
        for i, delete_leaving in enumerate(leaving):
            message['leaving'][i] = {}
            message['leaving'][i]['user_id'] = delete_leaving.user_id
            message['leaving'][i]['user_name'] = user_name(delete_leaving.user_id)
            message['leaving'][i]['content'] = delete_leaving.content
            message['leaving'][i]['time'] = delete_leaving.time.strftime('%Y-%m-%d')
            session.delete(delete_leaving)
            session.commit()

        sourceResponse = session.query(source_response).filter(source_response.user_id == user_id).all()
        for i, delete_sourceResponse in enumerate(sourceResponse):
            message['sourceResponse'][i] = {}
            message['sourceResponse'][i]['user_id'] = delete_sourceResponse.user_id
            message['sourceResponse'][i]['user_name'] = user_name(delete_sourceResponse.response_id)
            message['sourceResponse'][i]['content'] = delete_sourceResponse.content
            message['sourceResponse'][i]['time'] = delete_sourceResponse.time.strftime('%Y-%m-%d')
            session.delete(delete_sourceResponse)
        session.commit()
        return message
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
#messageAll
def messageAll_read(user_id):
    session = conn.dbsession()
    try:
        response = session.query(func.count('*')).select_from(message_response).filter(message_response.user_id == user_id).scalar()
        follow = session.query(func.count('*')).select_from(message_follow).filter(message_follow.user_id == user_id).scalar()
        leaving = session.query(func.count('*')).select_from(message_leaving).filter(message_leaving.target_id == user_id).scalar()
        sourceResponse = session.query(func.count('*')).select_from(source_response).filter(
            source_response.user_id == user_id).scalar()
        return (int(response) + int(follow) + int(leaving) + int(sourceResponse))
    except:
        session.rollback()
        session.close()
        return '0'
    finally:
        session.close()
#leavingMessage
def leavingMessage(user_id,target_id,content):
    session = conn.dbsession()
    try:
        result = leaving_message(user_id=user_id,target_id=target_id,content=content)
        session.add(result)
        result = message_leaving(user_id=user_id, target_id=target_id, content=content)
        session.add(result)
        session.commit()
    except:
        session.rollback()
        session.close()
    finally:
        session.close()

#user_name
def user_name(user_id):
    session = conn.dbsession()
    try:
        user_name = session.query(user.user_name).filter(user.id == user_id).with_lockmode('read').scalar()
        return user_name
    except:
        session.rollback()
        session.close()
    finally:
        session.close()

#delete
def delete_title(title_id):
    session = conn.dbsession()
    try:
        result = session.query(main).filter(main.title_id == title_id).all()
        for i in result:
            imgName = i.imgName.split('|')
            for path in imgName:
                try:
                    file = session.query(files).filter(files.name == path).first()
                    if file:
                        session.delete(file)
                        session.commit()
                    os.remove(UPLOAD_FOLDER+path)
                except:
                    session.delete(i)
                    session.commit()
                    continue
            session.delete(i)
            session.commit()
        result = session.query(detail).filter(detail.title_id == title_id).all()
        for i in result:
            for i in result:
                comment_result = session.query(main).filter(main.title_id == i.title_id).first()
                comment_result.comment -= 1
                session.commit()
                imgName = i.imgName.split('|')
                for path in imgName:
                    try:
                        file = session.query(files).filter(files.name == path).first()
                        if file:
                            session.delete(file)
                            session.commit()
                        os.remove(UPLOAD_FOLDER+path)
                    except:
                        continue
            session.delete(i)
            session.commit()
        result = session.query(comment).filter(comment.target_title_id == title_id).all()
        for i in result:
            comment_result = session.query(detail).filter(detail.id == i.detail_id).first()
            if comment_result:
                comment_result.comment -= 1
                session.delete(i)
                session.commit()
        result = session.query(message_response).filter(message_response.title_id == title_id).all()
        if result:
            for i in result:
                session.delete(i)
                session.commit()
        result = session.query(user_collection).filter(user_collection.title_id == title_id).all()
        if result:
            for i in result:
                session.delete(i)
                session.commit()
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
def delete_detail(detail_id):
    session = conn.dbsession()
    try:
        result = session.query(detail).filter(detail.id == detail_id).all()
        for i in result:
            comment_result = session.query(main).filter(main.title_id == i.title_id).first()
            if comment_result:
                comment_result.comment -= 1
                for ii in result:
                    imgName = ii.imgName.split('|')
                    for path in imgName:
                        try:
                            file = session.query(files).filter(files.name == path).first()
                            session.delete(file)
                            session.commit()
                            os.remove(UPLOAD_FOLDER+path)
                        except:
                            continue
            session.delete(i)
            session.commit()
        result = session.query(comment).filter(comment.detail_id == detail_id).all()
        for i in result:
            session.delete(i)
            session.commit()
        result = session.query(message_response).filter(message_response.detail_id == detail_id).all()
        for i in result:
            session.delete(i)
            session.commit()
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
def delete_comment(comment_id):
    session = conn.dbsession()
    try:
        result = session.query(comment).filter(comment.id == comment_id).all()
        for i in result:
            comment_result = session.query(detail).filter(detail.id == i.detail_id).first()
            comment_result.comment -= 1
            session.delete(i)
            session.commit()
        result = session.query(message_response).filter(message_response.comment_id == comment_id).all()
        for i in result:
            session.delete(i)
            session.commit()
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
def delete_collection(user_id,title_id):
    session = conn.dbsession()
    try:
        result = session.query(user_collection).filter(user_collection.user_id == user_id).filter(user_collection.title_id == title_id).first()
        if result:
            session.delete(result)
            session.commit()
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
def delete_leaving(user_id,id):
    session = conn.dbsession()
    try:
        result = session.query(leaving_message).filter(leaving_message.target_id == user_id).filter(leaving_message.id == id).first()
        if result:
            session.delete(result)
            session.commit()
        result = session.query(message_leaving).filter(message_leaving.target_id == user_id).filter(message_leaving.id == id).first()
        if result:
            session.delete(result)
            session.commit()
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
#####################################################################################
#资源

def ziYuan():
    session = conn.dbsession()
    try:
        result = session.query(source).order_by(source.browse.desc()).all()
        data = {}
        num = {}
        i = 0
        for d in result:
            if d.tag is None or d.tag is '':
                continue
            for tag in d.tag.split(','):
                d.subtitle = re.sub('(<img.*?>.*?</.*?>|<iframe.*?>.*?</.*?>|<video.*?>.*?</.*?>|<.*?>)', '',d.subtitle)
                if tag not in data:
                    data[tag] = {}
                    num[tag] = 1
                else:
                    if num[tag] == 6:
                        continue
                    num[tag] += 1
                data[tag][i] = {}
                data[tag][i]['id'] = d.id
                data[tag][i]['subtitle'] = (d.subtitle[0:70] + '[...]') if len(d.subtitle) > 69 else d.subtitle
                data[tag][i]['title'] = d.title
                data[tag][i]['user_id'] = d.user_id
                data[tag][i]['up_num'] = d.up_num
                data[tag][i]['comment'] = d.comment
                data[tag][i]['browse'] = int(d.browse/2)
                data[tag][i]['time'] = d.time.split(',')
                type = ''
                for item in d.type.split(','):
                    type += '<span><a title="{}" style="color:#ffffff" href="/lun_tan?zi_yuan_search_type=type&search={}">{}</a></span>'.format(item,item,item)
                data[tag][i]['type'] = type
                data[tag][i]['imgName'] = d.imgName
                data[tag][i]['new'] = json.loads(json.dumps(d.path0.split('@@')[-1].split('|')[-1]).replace('\\\\','\\'))
                i += 1
        return data
    except:
        session.rollback()
        session.close()
        return ziYuan()
    finally:
        session.close()
def ziYuanRead(start,num):
    session = conn.dbsession()
    try:
        result = session.query(source).limit(num).offset(start).all()
        data = {}
        for i, d in enumerate(result):
            d.subtitle = re.sub('(<img.*?>.*?</.*?>|<iframe.*?>.*?</.*?>|<video.*?>.*?</.*?>|<.*?>)', '', d.subtitle)
            data[i] = {}
            data[i]['id'] = d.id
            data[i]['title'] = d.title
            data[i]['subtitle'] = d.subtitle
            data[i]['user_id'] = d.user_id
            data[i]['up_num'] = d.up_num
            data[i]['comment'] = d.comment
            data[i]['browse'] = int(d.browse/2)
            data[i]['time'] = d.time.split(',')
            data[i]['type'] = d.type
            data[i]['imgName'] = d.imgName
            data[i]['path0'] = d.path0
        return data
    except:
        session.rollback()
        session.close()
        return ziYuanRead(start)
    finally:
        session.close()
import copy
def sourceRead(id):
    session = conn.dbsession()
    try:
        result = session.query(source).filter(source.id == id).first()
        result.subtitle = re.sub('(<img.*?>.*?</.*?>|<iframe.*?>.*?</.*?>|<video.*?>.*?</.*?>|<.*?>)', '', result.subtitle)
        data = copy.deepcopy(result)
        type = ''
        for item in data.type.split(','):
            type += '<span><a title="{}" style="color:#ffffff" href="/lun_tan?zi_yuan_search_type=type&search={}">{}</a></span>'.format(item, item, item)
        data.type = type
        result.browse += 1
        session.commit()
        return data
    except:
        session.rollback()
        session.close()
        return sourceRead(id)
    finally:
        session.close()
def sourceDetailRead(id):
    session = conn.dbsession()
    try:
        return session.query(source_detail).filter(source_detail.source_id == id).order_by(source_detail.source_id.desc()).all()
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
def source_recommend_read(id):
    session = conn.dbsession()
    try:
        year = session.query(source.year).filter(source.id == id).scalar()
        if year:
            count = session.query(func.count('*')).select_from(source).filter(source.year == year).order_by(source.browse.desc()).scalar()
            result = session.query(source).filter(source.year == year).order_by(source.browse.desc()).all()
        else:
            count = session.query(func.count('*')).select_from(source).order_by(source.browse.desc()).limit(1000).offset(0).scalar()
            result = session.query(source).limit(1000).offset(0).all()
        data = {}
        rand = []
        for i in range(14):
            n = random.randint(0, 25)
            if n not in rand:
                rand.append(n)
        for i, d in enumerate(result):
            if i not in rand:
                continue
            d.subtitle = re.sub('(<img.*?>.*?</.*?>|<iframe.*?>.*?</.*?>|<video.*?>.*?</.*?>|<.*?>)', '', d.subtitle)
            data[i] = {}
            data[i]['id'] = d.id
            data[i]['title'] = d.title
            data[i]['subtitle'] = d.subtitle
            data[i]['user_id'] = d.user_id
            data[i]['up_num'] = d.up_num
            data[i]['comment'] = d.comment
            data[i]['browse'] = int(d.browse / 2)
            data[i]['time'] = d.time.split(',')
            type = ''
            for item in d.type.split(','):
                type += '<span><a title="{}" style="color:#ffffff" href="/lun_tan?zi_yuan_search_type=type&search={}">{}</a></span>'.format(item, item, item)
            data[i]['type'] = type
            data[i]['imgName'] = d.imgName
        return data
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
def creat_source_detail(source_id,user_id,content):
    session = conn.dbsession()
    try:
        creat = source_detail(source_id=source_id, user_id=user_id, content=content, up_num=0, comment=0)
        session.add(creat)
        result = session.query(source).filter(source.id == source_id).first()
        result.comment += 1
        session.commit()
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
#source_comment读取
def source_comment_read(detail_id):
    session = conn.dbsession()
    try:
        result = session.query(source_comment).filter(source_comment.detail_id == detail_id).all()
        if result:
            return result
        return ''
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
# 新建source_comment
def creat_source_comment(detail_id,user_id,target_user_id,target_source_id,content):
    session = conn.dbsession()
    try:
        result = source_comment(detail_id = int(detail_id),user_id = int(user_id),target_source_id = int(target_source_id),target_user_id = int(target_user_id),content = content)
        session.add(result)
        session.flush()
        result_source_response = source_response(detail_id=detail_id,comment_id=result.id,user_id=target_user_id, response_id=user_id, content=content,source_id=target_source_id)
        session.add(result_source_response)
        updata = session.query(source_detail).filter(source_detail.id == detail_id).first()
        updata.comment = updata.comment + 1
        session.commit()
    except Exception as e:
        session.rollback()
        session.close()
    finally:
        session.close()
#tagRead
def tagRead():
    return session.query( source.tag, func.count('*').label('num')).group_by(source.tag).all()
#typeRead:
def typeRead():
    session = conn.dbsession()
    try:
        count = session.query(func.count('*')).select_from(source).scalar()
        result = session.query(source.type).limit(300).offset(random.randint(0, int(count))).all()
        data = {}
        re = {}
        for item in result:
            type_arr = item.type.split(',')
            for val in type_arr:
                if val is '' or val is None:
                    continue
                if val not in data:
                    data[val] = 1
                else:
                    data[val] += 1
        max = 0
        for i in data:
            if max < data[i]:
                max = data[i]
        for i,val in enumerate(data):
            re[i] = {}
            re[i]['label'] = val
            re[i]['value'] = 8+20*data[val]/max
            re[i]['href'] = '/lun_tan?zi_yuan_search_type=type&search=' + val
        return re
    except:
        session.rollback()
        session.close()
        return []
    finally:
        session.close()
#search
def zi_yuan_search(search,zi_yuan_search_type,sort):
    session = conn.dbsession()
    try:
        result = []
        if sort == 'browse':
            if zi_yuan_search_type == 'source':
                result = session.query(source).filter(source.title.like('%{search}%'.format(search=search))).order_by(source.browse.desc()).all()
            if zi_yuan_search_type == 'tag':
                result = session.query(source).filter(text('FIND_IN_SET("{0}",tag)'.format(search))).order_by(source.browse.desc()).all()
            if zi_yuan_search_type == 'type':
                result = session.query(source).filter(text('FIND_IN_SET("{0}",type)'.format(search))).order_by(source.browse.desc()).all()
            if zi_yuan_search_type == 'year':
                result = session.query(source).filter(source.year == search).order_by(source.browse.desc()).all()
        else:
            if zi_yuan_search_type == 'source':
                result = session.query(source).filter(source.title.like('%{search}%'.format(search=search))).order_by(source.year.desc()).all()
            if zi_yuan_search_type == 'tag':
                result = session.query(source).filter(text('FIND_IN_SET("{0}",tag)'.format(search))).order_by(source.year.desc()).all()
            if zi_yuan_search_type == 'type':
                result = session.query(source).filter(text('FIND_IN_SET("{0}",type)'.format(search))).order_by(source.year.desc()).all()
            if zi_yuan_search_type == 'year':
                result = session.query(source).filter(source.year == search).order_by(source.browse.desc()).all()
        data = {}
        for i, d in enumerate(result):
            d.subtitle = re.sub('(<img.*?>.*?</.*?>|<iframe.*?>.*?</.*?>|<video.*?>.*?</.*?>|<.*?>)','',d.subtitle)
            data[i] = {}
            data[i]['id'] = d.id
            data[i]['title'] = d.title
            data[i]['subtitle'] = (d.subtitle[0:70] + '[...]') if len(d.subtitle) > 69 else d.subtitle
            data[i]['user_id'] = d.user_id
            data[i]['up_num'] = d.up_num
            data[i]['comment'] = d.comment
            data[i]['browse'] = int(d.browse/2)
            data[i]['time'] = d.time.split(',')
            type = ''
            for item in d.type.split(','):
                type += '<span><a title="{}" style="color:#ffffff" href="/lun_tan?zi_yuan_search_type=type&search={}">{}</a></span>'.format(item, item, item)
            data[i]['type'] = type
            data[i]['imgName'] = d.imgName
        return data
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
#新建source_love
def source_love_creat(user_id,source_id):
    session = conn.dbsession()
    try:
        result_user = session.query(source_love).filter(source_love.user_id == user_id).filter(source_love.source_id == source_id).first()
        if result_user:
            source_up = session.query(source).filter(source.id == source_id).first()
            source_up.up_num -= 1
            session.delete(result_user)
            session.commit()
            return 'successT'
        else:
            source_up = session.query(source).filter(source.id == source_id).first()
            source_up.up_num += 1
            result = source_love(user_id=user_id, source_id=source_id)
            session.add(result)
            session.commit()
            return 'success'
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
#source_love_read
def source_love_read(user_id):
    session = conn.dbsession()
    try:
        data = session.query(source_love).filter(source_love.user_id == user_id).all()
        source_love_result = []
        for i,item in enumerate(data):
            source_love_result.append(item.source_id)
        return source_love_result
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
#time_tb
def time_tb():
    session = conn.dbsession()
    try:
        result = session.query(source).filter(text('FIND_IN_SET("新番连载",tag)')).order_by(source.year.desc()).all()
        data = {}
        num = {}
        i = 0
        for d in result:
            if d.tag is None or d.tag is '':
                continue
            for index,tag in enumerate(d.time.split(',')):
                if tag is None or tag is '':
                    continue
                tag = tag.strip()
                if tag not in data:
                    data[tag] = {}
                    num[tag] = 1
                else:
                    num[tag] += 1
                path_arr = d.path0.split('@@')
                u = 0
                number_name = 0
                for t,v in enumerate(path_arr):
                    number_name = index + 1 - u
                    if len(v.split('|')) > 1:
                        number_name = v.split('|')[-1]
                        if number_name is 'pv0':
                            u += 1
                        if number_name is 'pv1':
                            u += 1
                        if number_name is 'pv2':
                            u += 1
                d.subtitle = re.sub('(<img.*?>.*?</.*?>|<iframe.*?>.*?</.*?>|<video.*?>.*?</.*?>|<.*?>)', '',d.subtitle)
                data[tag][i] = {}
                data[tag][i]['number_name'] = number_name
                data[tag][i]['number'] = len(d.path0.split('@@'))-1
                data[tag][i]['id'] = d.id
                data[tag][i]['title'] = d.title
                data[tag][i]['subtitle'] = (d.subtitle[0:70] + '[...]') if len(d.subtitle) > 69 else d.subtitle
                data[tag][i]['user_id'] = d.user_id
                data[tag][i]['up_num'] = d.up_num
                data[tag][i]['comment'] = d.comment
                data[tag][i]['browse'] = int(d.browse / 2)
                data[tag][i]['time'] = d.time.split(',')
                data[tag][i]['num'] = d.path0.split('|')[-1]
                type = ''
                for item in d.type.split(','):
                    type += '<span><a title="{}" style="color:#ffffff" href="/lun_tan?zi_yuan_search_type=type&search={}">{}</a></span>'.format(item, item, item)
                data[tag][i]['type'] = type
                data[tag][i]['imgName'] = d.imgName
                i += 1

        sorted_x = sorted(data.items(), key=operator.itemgetter(0),reverse=True)
        return dict(sorted_x)
    except:
        session.rollback()
        session.close()
    finally:
        session.close()
#fen_lei
def fen_lei():
    session = conn.dbsession()
    try:
        result = session.query(source).all()
        data = {'时间':{},'类型':{}}
        res = {'时间':[],'类型':[]}
        for item in result:
            if item == '' or item is None:
                continue
            type_arr = item.type.split(',')
            for val in type_arr:
                if val == '' or val is None:
                    continue
                if val not in data['类型']:
                    data['类型'][val] = 1
                else:
                    data['类型'][val] += 1
            year_arr = item.year
            if year_arr is '' or year_arr is None:
                continue
            if year_arr not in data['时间']:
                data['时间'][year_arr] = 1
            else:
                data['时间'][year_arr] += 1
        data['时间'] = dict(sorted(data['时间'].items(), key=operator.itemgetter(0), reverse=True))
        for key,val in enumerate(data['类型']):
            res['类型'].append('<a title="{}" class="fenLenSpan" href="/lun_tan?zi_yuan_search_type=type&search={}">{}</a>'.format(
                val, val, val))
        for key,val in enumerate(data['时间']):
            res['时间'].append('<a title="{}" class="fenLenSpan" href="/lun_tan?zi_yuan_search_type=year&search={}">{}</a>'.format(
                val, val, val))
        return res
    except:
        session.rollback()
        session.close()
        return fen_lei()
    finally:
        session.close()
#source_read
def source_read(source_id):
    session = conn.dbsession()
    try:
        result = session.query(source).filter(source.id == source_id).first()
        result.subtitle = re.sub('(<img.*?>.*?</.*?>|<iframe.*?>.*?</.*?>|<video.*?>.*?</.*?>|<.*?>)', '', result.subtitle)
        return result
    except:
        session.rollback()
        session.close()
    finally:
        session.close()