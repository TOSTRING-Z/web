from py.mysql_conn import *
import os
import py.mysql_conn as connect
conn = connect.conn().obj_conn()
UPLOAD_FOLDER = '/root/PycharmProjects/wo_de_lun_tan'
#tem_upload
class tem_upload(conn.base):
    __tablename__ = 'tem_upload'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
#files
class files(conn.base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    name = Column(CHAR(50))
    type = Column(Text)
result = conn.session.query(tem_upload).all()
for i in result:
    imgName = i.name.split('|')
    for path in imgName:
        try:
            file = conn.session.query(files).filter(files.name == path).first()
            conn.session.delete(file)
            os.remove(UPLOAD_FOLDER+path)
        except:
            continue
    conn.session.delete(i)
conn.session.commit()