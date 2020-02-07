from flask import Flask,request,render_template,url_for,redirect,session,flash,Response,make_response
from functools import wraps
import py.sql as pysql
import json
from werkzeug.utils import secure_filename
import os
import re
import time
import random
from threading import Timer

UPLOAD_FOLDER = '/install/web/wo_de_lun_tan/static/public/upload/'
SUBMIT_FOLDER = '/install/web/wo_de_lun_tan/static/public/img/user/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif',''])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SUBMIT_FOLDER'] = SUBMIT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 2048 * 2048
class innerText:
    def first(html_in,pattern,split_sel):
        result = re.search(r'{0}'.format(str(pattern)), str(html_in), re.DOTALL)
        if result:
            result_groups = result.groups()
            return split_sel.join(result_groups)
        return None
    def all(html_in,pattern,split_sel):
        result = re.findall(r'{0}'.format(str(pattern)), str(html_in), re.DOTALL)
        if result:
            return split_sel.join(result)
        return None
all_ip = {}
def get_ip():
    try:
        header = request.headers
        ip = request.headers['X-Forwarded-For']
        if ip in all_ip:
            all_ip[ip] += 1
        else:
            all_ip[ip] = 1
        with open('/install/web/wo_de_lun_tan/static/public/ip/{}.txt'.format(ip),'a') as f:
            f.write('第{}次请求:\n{}'.format(all_ip[ip], header))
    except:
        print('err!')
         
#定义验证登陆装饰器
def login(func):
    @wraps(func)
    def wrappers(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return render_template('deng_lu.html')
    return wrappers
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

import py.xml as pyxml
@app.route('/sitemap')
@app.route('/sitemap.xml')
def sitemap():
    n = random.randint(0, 7000)
    data = pysql.ziYuanRead(n,1000)
    xml = pyxml.sitemap(data)
    return Response(xml, mimetype='text/xml')
@app.route('/root')
def root():
    user_id = session.get('user_id')
    if user_id == 1:
        return render_template("root.html")
    return redirect(url_for('deng_lu'))
#注册验证
@app.route('/zhu_ce_yan_zheng',methods=['POST'])
def zhu_ce_yan_zheng():
    if request.method == 'POST':
        user_name = request.form.get('username')
        password = request.form.get('password_1')
        zc_rs = pysql.zhu_ce_yan_zheng(user_name, password)
        if zc_rs:
            session['user_id'] = zc_rs.id
            session['user_name'] = str(zc_rs.user_name)
            session['vip'] = str(zc_rs.vip)
            session['sersonal_signature'] = str(zc_rs.sersonal_signature)
            return redirect('/zi_yuan')
        else:
            flash('用户已注册!')
            return redirect(url_for('zhu_ce'))
    return ''
#注册
@app.route('/zhu_ce')
def zhu_ce():
    return render_template('zhu_ce.html')
#登陆
@app.route('/deng_lu')
def deng_lu():
    return render_template('deng_lu.html')
#登陆验证
@app.route('/deng_lu_yan_zheng',methods=['POST'])
def deng_lu_yan_zheng():
    if request.method == 'POST':
        user_name = request.form.get('username')
        password = request.form.get('password')
        yz_rs = pysql.deng_lu_yan_zheng(user_name,password)
        switch = {
            0:'无该用户!',
            1:'密码错误!'
        }
        if yz_rs == 0:
            flash(switch[yz_rs])
            return render_template('deng_lu.html')
        elif yz_rs == 1:
            flash(switch[yz_rs])
            return render_template('deng_lu.html')
        else:
            try:
                session['user_id'] = yz_rs.id
                session['user_name'] = str(yz_rs.user_name)
                session['vip'] = str(yz_rs.vip)
                session['sersonal_signature'] = str(yz_rs.sersonal_signature)
                return redirect('/zi_yuan')
            except:
                flash('系统出错，请尝试重新登陆！')
                return render_template('deng_lu.html')
#注销
@app.route('/re_deng_lu')
def re_deng_lu():
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('vip', None)
    session.pop('sersonal_signature', None)
    return redirect('/zi_yuan')
#主页
@app.route('/home')
@app.route('/index')
def index():
    data = pysql.plate_read_all()
    
    if data:
        return render_template('index.html',data = data)
    return '请刷新重试...'
#用户面板
@app.route('/user/<user_id>')
@login
def user(user_id):
    user_data = pysql.user_read(user_id)
    user_follow_data = pysql.user_follow_read(user_id)
    user_follow = []
    for i, foo in enumerate(user_follow_data):
        user_follow.append(foo.follow_id)
    return render_template('user.html',user_data = user_data,user_follow = user_follow)
#修改信息
@app.route('/xiuGai/<user_id>')
@login
def xiuGai(user_id):
    if user_id == str(session.get('user_id')):
        user_data = pysql.user_read(user_id)
        return render_template('xiuGai.html', user_data = user_data)
    else:
        return render_template('template.html',template = '''<p>酱子是不行的哦!</p>''')

#修改信息提交
@app.route('/xiuGai/submit/<user_id>',methods=['POST','GET'])
@login
def xiuGaSubmit(user_id):
    password = request.form.get('password')
    name = request.form.get('user_name')
    if user_id == str(session.get('user_id')) and user_id is not None and password is not None:
        zc_rs = pysql.zhu_ce_yan_zheng(name, password)
        if zc_rs or user_id is not session.get('user_id'):
            sex = request.form.get('sex')
            birthday = request.form.get('birthday')
            phone = request.form.get('phone')
            email = request.form.get('email')
            hobbies = request.form.get('hobbies')
            sersonal_signature = request.form.get('sersonal_signature')
            pysql.user_information(user_id,name,password,sex,birthday,phone,email,hobbies,sersonal_signature)
            return '信息修改成功!'
        else:
            return '用户名以被使用!'
    else:
        return render_template('template.html',template = '''<p>酱子是不行的哦!</p>''')
#修改图片提交
@app.route('/xiuGai/image/<user_id>',methods=['POST'])
@login
def xiuGaiImage(user_id):
    if user_id == str(session.get('user_id')):
        if request.method == 'POST':
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = str(user_id) + '.png'
                file.save(os.path.join(app.config['SUBMIT_FOLDER'], filename))
                return os.path.join('/static/public/user/', filename)
    else:
        return '0'
#messageAll
@app.route('/messageAll')
def messageAll():
    if session.get('user_id'):
        result = pysql.messageAll_read(session.get('user_id'))
        re = str(result)
        return re
    else:
        return '0'
#message
@app.route('/message')
@login
def message():
    user_id = session.get('user_id')
    result = pysql.message_read(user_id)
    return json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))
#留言
@app.route('/leavingMessage/<target_id>',methods=['POST','GET'])
@login
def leavingMessage(target_id):
    content = request.form.get('content')
    if content:
        user_id = session.get('user_id')
        pysql.leavingMessage(user_id,target_id,content)
    return redirect('/user/{0}'.format(target_id))
#delete
@app.route('/deleteTitle/<title_id>/<user_id>')
def deleteTitle(title_id,user_id):
    if user_id == str(session.get('user_id')):
        pysql.delete_title(title_id)
    return redirect('/user/{0}'.format(user_id))
@app.route('/deleteDetail/<id>/<user_id>')
def deleteDetail(id,user_id):
    if user_id == str(session.get('user_id')):
        pysql.delete_detail(id)
    return redirect('/user/{0}'.format(user_id))
@app.route('/deleteComment/<id>/<user_id>')
def deleteComment(id,user_id):
    if user_id == str(session.get('user_id')):
        pysql.delete_comment(id)
    return redirect('/user/{0}'.format(user_id))
@app.route('/deleteCollection/<title_id>/<user_id>')
def deleteCollection(title_id,user_id):
    if user_id == str(session.get('user_id')):
        pysql.delete_collection(user_id,title_id)
    return redirect('/user/{0}'.format(user_id))
@app.route('/deleteFollow/<up_id>/<user_id>')
def deleteFollow(up_id,user_id):
    if user_id == str(session.get('user_id')):
        pysql.user_follow_creat(user_id=user_id,follow_id=up_id)
    return redirect('/user/{0}'.format(user_id))
@app.route('/deleteLeaving/<id>/<user_id>')
def deleteLeaving(user_id,id):
    if user_id == str(session.get('user_id')):
        pysql.delete_leaving(user_id,id)
    return redirect('/user/{0}'.format(user_id))

#用户选择
@app.route('/user_sel/<user_id>/<user_sel>')
@login
def user_sel(user_id,user_sel):
    user_name = pysql.user_name(user_id)
    if user_sel == '动态':
        data_table_main = []
        data = pysql.user_title_read(user_id)
        for i, foo in enumerate(data):
            foo.subtitle = re.sub('(<img.*?>.*?</.*?>|<iframe.*?>.*?</.*?>|<video.*?>.*?</.*?>|<.*?>)','',foo.subtitle)  #参数第一项模板，第二项为替换的值
            foo.subtitle = '{}[...]'.format(foo.subtitle[:50]) if len(foo.subtitle) > 49 else foo.subtitle
            img = ''
            for imgname in foo.imgName.split('|'):
                if imgname is not '' and img is '':
                    img = img + '<img style="height:150px;width;100%;object-fit: cover;" src="{0}!800-800" class="img-fluid"></img>'.format(imgname)
            d = {}
            d['main'] = \
            '<div class="media" id="'+foo.title+'" onclick="detail(this)">' \
                           '<div class="media-body">' \
                               '<div class="col-lg-12">' \
                                    '<h4><a  href="/lun_tan/detail/'+str(foo.title_id)+'">'+foo.title+'<a></h4>' \
                                    '<a href="/user/'+str(foo.up_id)+'" title="'+user_name+'"><img src="' + url_for('static', filename='public/img/user/' + str(foo.up_id))+ '.png!100-100"alt="' + user_name + '" class ="align-self-start mr-1 rounded-circle" style="width:20px;margin-top:-3px">' \
                                    ''+ user_name + '</a>' \
                                    '<span class="badge">&emsp;发表于:' + foo.creation_time.strftime('%Y-%m-%d') + '</span>' \
                               '</div>' \
                               '<div class="col-lg-12">' \
                                   '<div>'+img+'</div><p>'+foo.subtitle+'</p>' \
                               '</div>' \
                               '<div class="col-lg-12">' \
                                    '<button class="main-title-buttom"><svg style="top:4px" fill="currentColor" viewBox="0 0 24 24" width="1.2em" height="1.2em"><path d="M10.241 19.313a.97.97 0 0 0-.77.2 7.908 7.908 0 0 1-3.772 1.482.409.409 0 0 1-.38-.637 5.825 5.825 0 0 0 1.11-2.237.605.605 0 0 0-.227-.59A7.935 7.935 0 0 1 3 11.25C3 6.7 7.03 3 12 3s9 3.7 9 8.25-4.373 9.108-10.759 8.063z" fill-rule="evenodd"></path></svg>' + str(foo.comment) + '条评论</button>&nbsp;&nbsp;' \
                                    '<button class="main-title-buttom" id="up"><svg fill="currentColor" viewBox="0 0 24 24" width="10" height="10"><path d="M2 18.242c0-.326.088-.532.237-.896l7.98-13.203C10.572 3.57 11.086 3 12 3c.915 0 1.429.571 1.784 1.143l7.98 13.203c.15.364.236.57.236.896 0 1.386-.875 1.9-1.955 1.9H3.955c-1.08 0-1.955-.517-1.955-1.9z"></path></svg> 赞同 '+str(foo.up_num)+'</button>' \
                                    ''+( '' if  user_id != str(session.get('user_id')) else '<a style="margin-left:2em;" href="/deleteTitle/{0}/{1}"><i class="fa fa-trash-o" aria-hidden="true"></i></a>'.format(foo.title_id,user_id))+'' \
                               '</div>' \
                           '</div>' \
                        '</div>'
            data_table_main.append(d)
        if data_table_main == []:
            return ''
        return json.dumps(data_table_main, sort_keys=True, indent=4, separators=(',', ': '))
    if user_sel == '文章':
        data_table_main = []
        for i, foo in enumerate(pysql.user_title_read(user_id)):
            d = {}
            d['main'] = \
            '<div class="media" id="'+foo.title+'" onclick="detail(this)">' \
                           '<div class="media-body">' \
                               '<div class="col-lg-12">' \
                                    '<h4><a  href="/lun_tan/detail/'+str(foo.title_id)+'">'+foo.title+'<a></h4>' \
                                    '<a href="/user/'+str(foo.up_id)+'" title="'+user_name+'"><img src="' + url_for('static', filename='public/img/user/' + str(foo.up_id))+ '.png!100-100"alt="' + user_name + '" class ="align-self-start mr-1 rounded-circle" style="width:20px;margin-top:-3px">' \
                                    ''+ user_name + '</a>' \
                                    '<span class="badge">&emsp;发表于:' + foo.creation_time.strftime('%Y-%m-%d') + '</span>' \
                               '</div>' \
                               '<div class="col-lg-12">' \
                                    '<button class="main-title-buttom"><svg style="top:4px" fill="currentColor" viewBox="0 0 24 24" width="1.2em" height="1.2em"><path d="M10.241 19.313a.97.97 0 0 0-.77.2 7.908 7.908 0 0 1-3.772 1.482.409.409 0 0 1-.38-.637 5.825 5.825 0 0 0 1.11-2.237.605.605 0 0 0-.227-.59A7.935 7.935 0 0 1 3 11.25C3 6.7 7.03 3 12 3s9 3.7 9 8.25-4.373 9.108-10.759 8.063z" fill-rule="evenodd"></path></svg>' + str(foo.comment) + '条评论</button>&nbsp;&nbsp;' \
                                    '<button class="main-title-buttom" id="up" data-up='+str(request.cookies.get('{0}data-up{1}'.format(session.get('user_id'),str(foo.title_id))))+'><svg fill="currentColor" viewBox="0 0 24 24" width="10" height="10"><path d="M2 18.242c0-.326.088-.532.237-.896l7.98-13.203C10.572 3.57 11.086 3 12 3c.915 0 1.429.571 1.784 1.143l7.98 13.203c.15.364.236.57.236.896 0 1.386-.875 1.9-1.955 1.9H3.955c-1.08 0-1.955-.517-1.955-1.9z"></path></svg> 赞同 '+str(foo.up_num)+'</button>' \
                                    ''+( '' if  user_id != str(session.get('user_id')) else '<a style="margin-left:2em;" href="/deleteTitle/{0}/{1}"><i class="fa fa-trash-o" aria-hidden="true"></i></a>'.format(foo.title_id,user_id))+'' \
                               '</div>' \
                           '</div>' \
                        '</div>'
            data_table_main.append(d)
        if data_table_main == []:
            return ''
        return json.dumps(data_table_main, sort_keys=True, indent=4, separators=(',', ': '))
    if user_sel == '回复':
        data_table_main = []
        for i, foo in enumerate(pysql.user_comment_read(user_id)):
            target_user_name = pysql.user_name(foo.target_user_id)
            d = {}
            d['main'] = \
            '<div class="media">' \
                        '<div class="media-body">' \
                            '<a href="/user/'+str(foo.user_id)+'" title="'+user_name+'"><img src="' + url_for('static', filename='public/img/user/' + str(foo.user_id))+ '.png!100-100"alt="' + user_name + '" class ="align-self-start mr-1 rounded-circle" style="width:20px;margin-top:-3px">' + user_name + '</a>' \
                            '<span class="badge">&emsp;发表于:' + foo.time.strftime('%Y-%m-%d') + '</span>' \
                            '<br><br>' \
                            '<p>回复<b style="color:#007bff"><a href="/user/'+str(foo.target_user_id)+'">@'+target_user_name+':</a></b>' + str(foo.content) + '</p>' \
                            '<div class="col-lg-12"><a href id="'+str(foo.id)+'" onclick="modalData(this)" data-detail_id="'+str(foo.detail_id)+'" data-target_title_id="'+str(foo.target_title_id)+'" data-user_id="'+str(foo.user_id)+'" class="main-title-buttom" data-toggle="modal" data-target="#Modal"><svg style="margin:0 5px;top:2px" fill="currentColor" viewBox="0 0 24 24" width="16" height="16"><path d="M22.959 17.22c-1.686-3.552-5.128-8.062-11.636-8.65-.539-.053-1.376-.436-1.376-1.561V4.678c0-.521-.635-.915-1.116-.521L1.469 10.67a1.506 1.506 0 0 0-.1 2.08s6.99 6.818 7.443 7.114c.453.295 1.136.124 1.135-.501V17a1.525 1.525 0 0 1 1.532-1.466c1.186-.139 7.597-.077 10.33 2.396 0 0 .396.257.536.257.892 0 .614-.967.614-.967z" fill-rule="evenodd"></path></svg>回复</a>' \
                            '&nbsp;&nbsp<a href="/lun_tan/detail/'+str(foo.target_title_id)+'""><i class="fa fa-external-link-square" aria-hidden="true"></i>&nbsp;跳转</a>' \
                            ''+( '' if  user_id != str(session.get('user_id')) else '<a style="margin-left:2em;" href="/deleteComment/{0}/{1}"><i class="fa fa-trash-o" aria-hidden="true"></i></a></div>'.format(foo.id,user_id))+'' \
                        '</div>' \
                    '</div>'
            data_table_main.append(d)
        if data_table_main == []:
            return ''
        return json.dumps(data_table_main, sort_keys=True, indent=4, separators=(',', ': '))
    if user_sel == '评论':
        data_table_main = []
        for i, foo in enumerate(pysql.user_detail_read(user_id)):
            d = {}
            d['main'] = \
            '<div class="media">' \
                            '<div class="media-body">' \
                            '<a href="/user/'+str(foo.message_user_id)+'"><img src="' + url_for('static', filename='public/img/user/' + str(foo.message_user_id))+ '.png!100-100"alt="' + user_name + '" class ="align-self-start mr-1 rounded-circle" style="width:20px;margin-top:-3px">' + user_name + '</a>' \
                            '<span class="badge">&emsp;发表于:' + foo.message_time.strftime('%Y-%m-%d') + '</span>' \
                            '<br><br><br>' \
                            '<p>' + foo.message_content + '</p>' \
                            '<div class="light-a">' \
                            '<button type="button" class="main-title-buttom">' \
                              '<svg style="margin:0 3px;top:4px" fill="currentColor" viewBox="0 0 24 24" width="1.2em" height="1.2em"><path d="M10.241 19.313a.97.97 0 0 0-.77.2 7.908 7.908 0 0 1-3.772 1.482.409.409 0 0 1-.38-.637 5.825 5.825 0 0 0 1.11-2.237.605.605 0 0 0-.227-.59A7.935 7.935 0 0 1 3 11.25C3 6.7 7.03 3 12 3s9 3.7 9 8.25-4.373 9.108-10.759 8.063z" fill-rule="evenodd"></path></svg>' \
                            '</button><a onclick="comment(this)" data-detail_id="'+str(foo.id)+'" data-title_id="'+str(foo.title_id)+'">' + str(foo.comment) + '条评论</a>' \
                                                        '&nbsp;&nbsp<a href="/lun_tan/detail/'+str(foo.title_id)+'"><i class="fa fa-external-link-square" aria-hidden="true"></i>&nbsp;跳转</a>' \
                            ''+( '' if  user_id != str(session.get('user_id')) else '<a style="margin-left:2em;" href="/deleteDetail/{0}/{1}"><i class="fa fa-trash-o" aria-hidden="true"></i></a></div>'.format(foo.id,user_id))+'' \
                        '</div>' \
                    '</div></div><br>' \
                    '<div style="display:none" id="'+str(foo.id)+'">' \
                    '</div>'
            data_table_main.append(d)
        if data_table_main == []:
            return ''
        return json.dumps(data_table_main, sort_keys=True, indent=4, separators=(',', ': '))

    if user_sel == '留言':
        if user_id != str(session.get('user_id')):
            return ''
        data_table_main = []
        for i, foo in enumerate(pysql.leaving_message_read(user_id)):
            d = {}
            user_name = pysql.user_name(foo.user_id)
            d['main'] = \
            '<div class="media">' \
                        '<div class="media-body">' \
                            '<a href="/user/'+str(foo.user_id)+'"><img src="' + url_for('static', filename='public/img/user/' + str(foo.user_id))+ '.png!100-100"alt="' + user_name + '" class ="align-self-start mr-1 rounded-circle" style="width:20px;margin-top:-3px">' + user_name + '</a>' \
                            '<span class="badge">&emsp;发表于:' + foo.time.strftime('%Y-%m-%d') + '</span>' \
                            '<br><br>' \
                            '<p>' + foo.content + '</p>' \
                            '<div class="light-a">' \
                            '<a style="position:absolute;right:0px;top:30px" href="/deleteLeaving/'+str(foo.id)+'/'+str(user_id)+'"><i class="fa fa-trash-o" aria-hidden="true"></i></a></div>' \
                        '</div>'
            data_table_main.append(d)
        if data_table_main == []:
            return ''
        return json.dumps(data_table_main, sort_keys=True, indent=4, separators=(',', ': '))
    if user_sel == '收藏':
        if user_id != str(session.get('user_id')):
            return ''
        data_table_main = []
        for i, foo in enumerate(pysql.user_collection_read(user_id)):
            d = {}
            d['main'] = '<div class="media">' \
                '<div class="media-body">' \
                '<h4><a href="/lun_tan/detail/'+str(foo.title_id)+'" title="'+foo.title_name+'">' + foo.title_name + '</a></h4>' \
                ''+( '' if  user_id != str(session.get('user_id')) else '<a style="position:absolute;right:0px;top:8px" href="/deleteCollection/{0}/{1}"><i class="fa fa-trash-o" aria-hidden="true"></i></a>'.format(foo.title_id,user_id))+'' \
                '</div>' \
            '</div>'
            data_table_main.append(d)
        if data_table_main == []:
            return ''
        return json.dumps(data_table_main, sort_keys=True, indent=4, separators=(',', ': '))
    if user_sel == '关注':
        if user_id != str(session.get('user_id')):
            return ''
        data_table_main = []
        for i, foo in enumerate(pysql.user_follow_read(user_id)):
            user_name = pysql.user_name(foo.follow_id)
            d = {}
            d['main'] = '<div class="media">' \
                '<div class="media-body">' \
                '<a href="/user/'+str(foo.follow_id)+'"><img src="' + url_for('static', filename='public/img/user/' + str(foo.follow_id))+ '.png!100-100"alt="' + user_name + '" class ="align-self-start mr-1 rounded-circle" style="width:20px;margin-top:-3px">' + user_name + '</a>' \
                ''+( '' if  user_id != str(session.get('user_id')) else '<a style="position:absolute;right:0px;top:0px" href="/deleteFollow/{0}/{1}"><i class="fa fa-trash-o" aria-hidden="true"></i></a>'.format(foo.follow_id,user_id))+'' \
                '</div>' \
            '</div>'
            data_table_main.append(d)
        if data_table_main == []:
            return ''
        return json.dumps(data_table_main, sort_keys=True, indent=4, separators=(',', ': '))
    if user_sel == '喜欢':
        if user_id != str(session.get('user_id')):
            return ''
        data = []
        for source_id in pysql.source_love_read(user_id):
            source = pysql.source_read(source_id)
            d = {}
            d['id'] = source.id
            d['title'] = source.title
            d['up_num'] = source.up_num
            d['comment'] = source.comment
            d['browse'] = source.browse
            d['imgName'] = source.imgName
            type = ''
            for item in source.type.split(','):
                type += '<span><a style="color:#ffffff" href="/lun_tan?zi_yuan_search_type=type&search={0}">{1}</a></span>'.format(
                    item, item)
            d['type'] = type
            data.append(d)
        if data == []:
            return ''
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
#论坛路由
@app.route('/lun_tan',methods=['GET'])
def lun_tan():
    if request.method == 'GET':
        zi_yuan_search_type = request.values.get('zi_yuan_search_type')
        if zi_yuan_search_type:
            search = request.values.get('search')
            sort = request.values.get('sort')
            result = pysql.zi_yuan_search(search,zi_yuan_search_type,sort)
            if result != {}:
                return render_template('zi_yuan/search_sourch.html',search = search,data = json.dumps(result, sort_keys=True, indent=4, separators=(',', ': ')))
            return render_template('zi_yuan/search_sourch.html',data = '')
        plate_id = request.values.get('plate_id')
        plate = pysql.plate_read(plate_id)
        if plate is None:
            plate = {}
            plate['id'] = plate_id
        classification = pysql.classification_read(plate_id)
        if classification is '':
            classification = []
        class quanBu:
            type = 'quan_bu'
            type_name = '全部'
            plate_id = request.values.get('plate_id')
        classification.append(quanBu)
        type = request.values.get('type')
        search = request.values.get('search')
        data = pysql.main_read(plate_id = plate_id,type = type,search = search)
        data_all = pysql.main_read(plate_id = plate_id,type='quan_bu',search = search)
        num = {}
        num['quan_bu'] = 0
        for foo in data_all:
            if foo.type not in num:
                num[foo.type] = 0
            num[foo.type] = num[foo.type] + 1
            num['quan_bu'] = num['quan_bu'] + 1
        dataCloud = {}
        for i,item in enumerate(classification):
            dataCloud[i] = {}
            dataCloud[i]['label'] = item.type_name
            if item.type in num and num['quan_bu'] is not 0:
                dataCloud[i]['value'] = 10+40*num[item.type]/num['quan_bu']
            else:
                dataCloud[i]['value'] = 20
            dataCloud[i]['href'] = '/lun_tan?plate_id={0}&type={1}'.format(item.plate_id,item.type)
        data_table_main = []
        for i, foo in enumerate(data):
            foo.subtitle = re.sub('(<img.*?>.*?</.*?>|<iframe.*?>.*?</.*?>|<video.*?>.*?</.*?>|<.*?>)', '',foo.subtitle)
            foo.subtitle = '{}[...]'.format(foo.subtitle[:50]) if len(foo.subtitle) > 49 else foo.subtitle
            user_data = pysql.user_read(foo.up_id)
            img = ''
            for imgname in foo.imgName.split('|'):
                if imgname is not '' and img is '':
                    img = img + '<img style="height:150px;width;100%;object-fit: cover;" src="{0}!800-800" class="img-fluid"></img>'.format(imgname)
            d = {}
            cookie = str(request.cookies.get('{0}data-up{1}'.format(session.get('user_id'),str(foo.title_id))))
            d['main'] = '<div class="media" id="'+foo.title+'" onclick="detail(this)">' \
                           '<div class="media-body">' \
                               '<div class="col-lg-12">' \
                                    '<h4><a href="/lun_tan/detail/'+str(foo.title_id)+'" title="'+foo.title+'">'+foo.title+'<a></h4>' \
                                    '<a href="/user/'+str(foo.up_id)+'"><img src="' + url_for('static', filename='public/img/user/' + str(foo.up_id))+ '.png!100-100"alt="' + user_data.user_name + '" class ="align-self-start mr-1 rounded-circle" style="width:20px;margin-top:-3px">' \
                                    ''+ user_data.user_name + '</a>' \
                                    '<div class="lv"><span class="lv-1" style="background-color:'+user_data.color+'">Lv</span><span class="lv-2" style="background-color:'+user_data.color+'">'+str(user_data.level)+'</span></div><span class="badge">&emsp;发表于:' + foo.creation_time.strftime('%Y-%m-%d') + '</span>' \
                                    '<br><br>' \
                               '</div>' \
                               '<div class="col-lg-12">' \
                                   '<div>'+img+'</div><p>'+foo.subtitle+'</p>' \
                               '</div>' \
                               '<div class="col-lg-12">' \
                                    '<button class="main-title-buttom"><svg style="top:4px" fill="currentColor" viewBox="0 0 24 24" width="1.2em" height="1.2em"><path d="M10.241 19.313a.97.97 0 0 0-.77.2 7.908 7.908 0 0 1-3.772 1.482.409.409 0 0 1-.38-.637 5.825 5.825 0 0 0 1.11-2.237.605.605 0 0 0-.227-.59A7.935 7.935 0 0 1 3 11.25C3 6.7 7.03 3 12 3s9 3.7 9 8.25-4.373 9.108-10.759 8.063z" fill-rule="evenodd"></path></svg>' + str(foo.comment) + '条评论</button>&nbsp;&nbsp;' \
                                    '<button class="main-title-buttom" id="up" data-up='+str(request.cookies.get('{0}data-up{1}'.format(session.get('user_id'),str(foo.title_id))))+'><svg fill="currentColor" viewBox="0 0 24 24" width="10" height="10"><path d="M2 18.242c0-.326.088-.532.237-.896l7.98-13.203C10.572 3.57 11.086 3 12 3c.915 0 1.429.571 1.784 1.143l7.98 13.203c.15.364.236.57.236.896 0 1.386-.875 1.9-1.955 1.9H3.955c-1.08 0-1.955-.517-1.955-1.9z"></path></svg> 赞同 '+str(foo.up_num)+'</button>' \
                               '</div>' \
                           '</div>' \
                        '</div>'
            data_table_main.append(d)
        data_table_main = json.dumps(data_table_main, sort_keys=True, indent=4, separators=(',', ': '))
        dataCloud = json.dumps(dataCloud, sort_keys=True, indent=4, separators=(',', ': '))
        return render_template('lun_tan/main.html',plate = plate,data = data_table_main,search = search,sel = type,classification = classification,num = num,dataCloud = dataCloud)
#detail
@app.route('/lun_tan/detail/<title_id>')
def detail(title_id):
    user_id = session.get('user_id')
    if user_id:
        user_follow_data = pysql.user_follow_read(user_id)
    else:
        user_follow_data = []
    user_follow = []
    for i, foo in enumerate(user_follow_data):
        user_follow.append(foo.follow_id)
    user_collection_data = pysql.user_collection_read(user_id)
    user_collection = []
    for i, foo in enumerate(user_collection_data):
        user_collection.append(foo.title_id)
    detail_main = pysql.detail_main_read(title_id=title_id)
    detail_main.description = re.sub('(<img.*?>.*?</.*?>|<iframe.*?>.*?</.*?>|<video.*?>.*?</.*?>|<.*?>)', '', detail_main.subtitle)
    detail = pysql.detail_read(title_id=title_id)
    data_table_main = []
    for i, foo in enumerate(detail):
        user_data = pysql.user_read(foo.message_user_id)
        d = {}
        d['main'] = '<div class="media">' \
                        '<div class="media-body">' \
                            '<a href="/user/'+str(foo.message_user_id)+'"><img src="' + url_for('static', filename='public/img/user/' + str(foo.message_user_id))+ '.png!100-100"alt="' + user_data.user_name + '" class ="align-self-start mr-1 rounded-circle" style="width:20px;margin-top:-3px">' + user_data.user_name + '</a>' \
                            '<div class="lv"><span class="lv-1" style="background-color:'+user_data.color+'">Lv</span><span class="lv-2" style="background-color:'+user_data.color+'">'+str(user_data.level)+'</span></div><span class="badge">&emsp;发表于:' + foo.message_time.strftime('%Y-%m-%d') + '</span>' \
                            '<br><br><br>' \
                            '<p>' + foo.message_content + '</p>' \
                            '<div class="light-a">' \
                            '<button type="button" class="main-title-buttom">' \
                            '<svg style="margin:0 3px;top:4px" fill="currentColor" viewBox="0 0 24 24" width="1.2em" height="1.2em"><path d="M10.241 19.313a.97.97 0 0 0-.77.2 7.908 7.908 0 0 1-3.772 1.482.409.409 0 0 1-.38-.637 5.825 5.825 0 0 0 1.11-2.237.605.605 0 0 0-.227-.59A7.935 7.935 0 0 1 3 11.25C3 6.7 7.03 3 12 3s9 3.7 9 8.25-4.373 9.108-10.759 8.063z" fill-rule="evenodd"></path></svg>' \
                            '</button><a onclick="comment(this)" data-detail_id="'+str(foo.id)+'" data-title_id="'+str(foo.title_id)+'">' + str(foo.comment) + '条评论</a>' \
                            '<a style="margin-left: 5px;" onclick="modalData(this)" data-target_title_id="' + str(foo.title_id) + '" data-detail_id="' + str(foo.id) + '" data-user_id="' + str(foo.message_user_id) + '" class="main-title-buttom" data-toggle="modal" data-target="#Modal"><svg style="margin:0 5px;top:2px" fill="currentColor" viewBox="0 0 24 24" width="16" height="16"><path d="M22.959 17.22c-1.686-3.552-5.128-8.062-11.636-8.65-.539-.053-1.376-.436-1.376-1.561V4.678c0-.521-.635-.915-1.116-.521L1.469 10.67a1.506 1.506 0 0 0-.1 2.08s6.99 6.818 7.443 7.114c.453.295 1.136.124 1.135-.501V17a1.525 1.525 0 0 1 1.532-1.466c1.186-.139 7.597-.077 10.33 2.396 0 0 .396.257.536.257.892 0 .614-.967.614-.967z" fill-rule="evenodd"></path></svg>回复</a>' \
                            '</div>' \
                        '</div>' \
                    '</div><br>' \
                    '<div style="display:none" id="slide'+str(foo.id)+'">' \
                    '</div>'
        data_table_main.append(d)
    return render_template('lun_tan/detail.html',title_id = title_id,detail_main = detail_main,data = data_table_main,user_follow = user_follow,user_collection = user_collection)
#新建讨论
@app.route('/xin_jian_tao_lun_html/<plate_id>/<sel>')
@login
def xin_jian_tao_lun_html(plate_id,sel):
    classification = pysql.classification_read(plate_id)
    return render_template('lun_tan/xin_jian_tao_lun.html',plate_id = plate_id,classification = classification,sel = sel)

@app.route('/xin_jian_tao_lun/<plate_id>',methods=['POST'])
@login
def xin_jian_tao_lun(plate_id):
    if request.method == 'POST':
        up_id = session.get('user_id')
        title = request.form.get('title')
        type = request.form.get('type')
        subtitle = request.form.get('subtitle')
        imgName = ''
        imgArr = re.finditer(r'src="(.*?)"',subtitle)
        for img in imgArr:
            imgName = imgName + '|' + img.group()[5:-1]
        pysql.creat_discuss(plate_id,up_id,type,title,subtitle,imgName)
        return redirect('/lun_tan?plate_id={0}&type={1}'.format(plate_id,type))
    return ''
#detail回复
@app.route('/detail_message',methods=['POST'])
@login
def detail_message():
    if request.method == 'POST':
        user_id = session.get('user_id')
        up_id = request.form.get('up_id')
        title_id = request.form.get('title_id')
        content = request.form.get('content')
        imgName = ''
        imgArr = re.finditer(r'src="(.*?)"',content)
        for img in imgArr:
            imgName = imgName + '|' + img.group()[5:-1]
        pysql.creat_detail(user_id,up_id,title_id,content,imgName)
        return redirect('/lun_tan/detail/{0}'.format(title_id))
    return ''

#comment读取
@app.route('/comment/<detail_id>')
def comment(detail_id):
    data = pysql.comment_read(detail_id)
    data_table_main = []
    for i, foo in enumerate(data):
        user_data = pysql.user_read(foo.user_id)
        target_user_name = pysql.user_name(foo.target_user_id)
        d = {}
        d['main'] = u'<div class="media">' \
                        '<div class="media-body">' \
                            '<a href="/user/'+str(foo.user_id)+'"><img src="' + url_for('static', filename='public/img/user/' + str(foo.user_id))+ '.png!100-100"alt="' + user_data.user_name + '" class ="align-self-start mr-1 rounded-circle" style="width:20px;margin-top:-3px">' + user_data.user_name + '</a>' \
                            '<div class="lv"><span class="lv-1" style="background-color:'+user_data.color+'">Lv</span><span class="lv-2" style="background-color:'+user_data.color+'">'+str(user_data.level)+'</span></div><span class="badge">&emsp;发表于:' + foo.time.strftime('%Y-%m-%d') + '</span>' \
                            '<br><br>' \
                            '<p>回复<b style="color:#007bff"><a href="/user/'+str(foo.target_user_id)+'">@'+target_user_name+':</a></b>' + str(foo.content) + '</p>' \
                            '<div class="col-lg-12"><a href id="'+str(foo.id)+'" onclick="modalData(this)" data-detail_id="'+str(foo.detail_id)+'" data-target_title_id="'+str(foo.target_title_id)+'" data-user_id="'+str(foo.user_id)+'" class="main-title-buttom" data-toggle="modal" data-target="#Modal"><svg style="margin:0 5px;top:2px" fill="currentColor" viewBox="0 0 24 24" width="16" height="16"><path d="M22.959 17.22c-1.686-3.552-5.128-8.062-11.636-8.65-.539-.053-1.376-.436-1.376-1.561V4.678c0-.521-.635-.915-1.116-.521L1.469 10.67a1.506 1.506 0 0 0-.1 2.08s6.99 6.818 7.443 7.114c.453.295 1.136.124 1.135-.501V17a1.525 1.525 0 0 1 1.532-1.466c1.186-.139 7.597-.077 10.33 2.396 0 0 .396.257.536.257.892 0 .614-.967.614-.967z" fill-rule="evenodd"></path></svg>回复</a>' \
                            '</div>' \
                        '</div>' \
                    '</div>'
        data_table_main.append(d)
    data_table_main = json.dumps(data_table_main, sort_keys=True, indent=4, separators=(',', ': '))
    if data_table_main == []:
        data_table_main = ''
    return data_table_main
#conmmen回复
@app.route('/conmment_response',methods=['POST'])
@login
def conmment_response():
    if request.method == 'POST':
        detail_id = request.form.get('detail_id')
        target_user_id = request.form.get('user_id')
        user_id = session.get('user_id')
        target_title_id = request.form.get('target_title_id')
        content = request.form.get('content')
        pysql.creat_comment(detail_id,user_id,target_user_id,target_title_id,content)
        return redirect('/lun_tan/detail/{0}'.format(target_title_id))
    return ''
#/upload/img
@app.route('/uploadMain',methods=['POST'])
@login
def uploadMain():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            while 1:
                if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'],'{0}'.format(filename))):
                    filename = '_'+str(filename)
                else:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'],'{0}'.format(filename)))
                    pysql.creat_file(os.path.join('/static/public/upload/','{0}'.format(filename)),filename.rsplit('.', 1)[1])
                    return os.path.join('/static/public/upload/','{0}'.format(filename))
    return ''
@app.route('/uploadDetail',methods=['POST'])
@login
def uploadDetail():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            while 1:
                if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'],'{0}'.format(filename))):
                    filename = '_'+str(filename)
                else:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'],'{0}'.format(filename)))
                    pysql.creat_file(os.path.join('/static/public/upload/','{0}'.format(filename)),filename.rsplit('.', 1)[1])
                    return os.path.join('/static/public/upload/','{0}'.format(filename))
    return ''
#留言板
@app.route('/detail_main_up_down/<title_id>/<type>')
def detail_main_up_down(title_id,type):
    if session.get('user_id'):
        result = pysql.detail_main_up_down_result(title_id,type)
        return str(result)
    return ''

#留言板
@app.route('/liu_yan_ban')
@login
def liu_yan_ban():
    return render_template("liu_yan_ban.html")
#留言操作
@app.route('/liu_yan/<param>',methods=['POST','GET'])
@login
def liu_yan(param):
    message_user_id = request.values.get('message_user_id')
    message_content = request.values.get('message_content')
    time = request.values.get('time')
    if param == 'fa_song':
        data_rs = pysql.detail_send(message_user_id,message_content)
        return data_rs
    if param == 'du_qu':
        data_rs = pysql.detail_read(message_user_id)
        return data_rs
    if param == 'shan_chu':
        data_rs = pysql.detail_delete(message_user_id)
        return data_rs
    return ''

#收藏
@app.route('/shouCang/<title_id>/<title_name>',methods=['POST','GET'])
@login
def shouCang(title_id,title_name):
    user_id = session.get('user_id')
    return pysql.user_collection_creat(user_id,title_id,title_name)
#关注
@app.route('/guanZhu/<up_id>')
@login
def guanZhu(up_id):
    user_id = session.get('user_id')
    return pysql.user_follow_creat(user_id=user_id,follow_id=up_id)
#cookin
from datetime import *
@app.route('/set_cookie/<user_id>/<title_id>/<type>')
def set_cookie(user_id,type,title_id):
    if session.get('user_id'):
        resp = Response("服务器返回信息")
        expires = datetime.now() + timedelta(days=30,hours=16)
        resp.set_cookie('{0}data-up{1}'.format(user_id,title_id), type, expires=expires)
        return resp
    resp = Response("服务器返回信息")
    expires = datetime.now() + timedelta(days=30,hours=16)
    resp.set_cookie('{0}data-up{1}'.format(user_id,title_id), '', expires=expires)
    return resp

###################################资源###########################################
#资源
@app.route('/zi_yuan')
@app.route('/')
def zi_yuan():
    get_ip()
    data_time = pysql.time_tb() or []
    data = pysql.ziYuan()
    dataCloud = pysql.typeRead()
    return render_template("zi_yuan/zi_yuan.html",data = data,dataCloud = dataCloud,data_time = data_time)
#资源server
@app.route('/zi_yuan_read/<start>')
def zi_yuan_read(start):
    result = pysql.ziYuanRead(start)
    if result != {}:
        return json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))
    return ''
@app.route('/owoSubmit/<source_id>/<come>/<num>',methods=['POST'])
def owoSubmit(source_id,come,num):
    user_id = session.get('user_id')
    if request.method == 'POST':
        if user_id:
            content = request.form.get('content')
            pysql.creat_source_detail(source_id,user_id,content)
            return redirect("/ziYuanDetail/{0}/{1}/{2}".format(source_id,come,num))
        return render_template('deng_lu.html')
#资源detail
@app.route('/ziYuanDetail/<id>/<come>/<num>')
def ziYuanDetail(id,come,num):
    get_ip()
    result = pysql.sourceRead(id)
    source_recommend = pysql.source_recommend_read(id)
    data = pysql.sourceDetailRead(id) or []

    user_id = session.get("user_id")
    source_love = []
    if user_id:
        source_love = pysql.source_love_read(user_id) or []
    detail = []
    for i, foo in enumerate(data):
        foo.content = foo.content.replace('&[','<img style="width:20px" src="/static/public/OwO/aLu/').replace(']&','.png">')
        user_data = pysql.user_read(foo.user_id)
        d = {}
        d['main'] = '<div class="media">' \
                        	'<div class="media-body">' \
                            	'<a href="/user/'+str(foo.user_id)+'"><img src="' + url_for('static', filename='public/img/user/' + str(foo.user_id))+ '.png!100-100"alt="' + user_data.user_name + '" class ="align-self-start mr-1 rounded-circle" style="width:20px;margin-top:-3px">' + user_data.user_name + '</a>' \
                            	'<div class="lv"><span class="lv-1" style="background-color:'+user_data.color+'">Lv</span><span class="lv-2" style="background-color:'+user_data.color+'">'+str(user_data.level)+'</span></div><span class="badge">&emsp;发表于:' + foo.time.strftime('%Y-%m-%d') + '</span>' \
                            	'<br><br><br>' \
                            	'<p>' + foo.content + '</p>' \
                            	'<div class="light-a">' \
                            	'<button type="button" class="main-title-buttom">' \
                              	'<svg style="margin:0 3px;top:4px" fill="currentColor" viewBox="0 0 24 24" width="1.2em" height="1.2em"><path d="M10.241 19.313a.97.97 0 0 0-.77.2 7.908 7.908 0 0 1-3.772 1.482.409.409 0 0 1-.38-.637 5.825 5.825 0 0 0 1.11-2.237.605.605 0 0 0-.227-.59A7.935 7.935 0 0 1 3 11.25C3 6.7 7.03 3 12 3s9 3.7 9 8.25-4.373 9.108-10.759 8.063z" fill-rule="evenodd"></path></svg>' \
                            	'</button><a onclick="comment(this)" data-detail_id="'+str(foo.id)+'" data-source_id="'+str(foo.source_id)+'">' + str(foo.comment) + '条评论</a>' \
                            	'<a style="margin-left: 5px;" onclick="modalData(this)" data-target_source_id="' + str(foo.source_id) + '" data-detail_id="' + str(foo.id) + '" data-user_id="' + str(foo.user_id) + '" class="main-title-buttom" data-toggle="modal" data-target="#Modal"><svg style="margin:0 5px;top:2px" fill="currentColor" viewBox="0 0 24 24" width="16" height="16"><path d="M22.959 17.22c-1.686-3.552-5.128-8.062-11.636-8.65-.539-.053-1.376-.436-1.376-1.561V4.678c0-.521-.635-.915-1.116-.521L1.469 10.67a1.506 1.506 0 0 0-.1 2.08s6.99 6.818 7.443 7.114c.453.295 1.136.124 1.135-.501V17a1.525 1.525 0 0 1 1.532-1.466c1.186-.139 7.597-.077 10.33 2.396 0 0 .396.257.536.257.892 0 .614-.967.614-.967z" fill-rule="evenodd"></path></svg>回复</a>' \
                            	'</div>' \
                        	'</div>' \
                    	'</div><br>' \
                    	'<div style="display:none" id="slide'+str(foo.id)+'">' \
                    	'</div>'
        detail.append(d)
    detail = json.dumps(detail, sort_keys=True, indent=4, separators=(',', ': '))
    if detail == '[]':
        detail = ''
    try:
        num = int(num)
    except:
        num = 0
    if come == '0':
        result.path = result.path0
    if come == '1':
        result.path = result.path1
    if come == '2':
        result.path = result.path2
    if come == '3':
        result.path = result.path3
    if come == '4':
        result.path = result.path4
    if come == '5':
        result.path = result.path5
    result.path_arr = [0]
    try:
        result.path_arr = result.path.split('@@')[num].split('|')
        result.path_arr[-1] = json.loads(json.dumps(result.path_arr[-1]).replace('\\\\','\\'))
        return render_template("zi_yuan/zi_yuan_detail.html",source_recommend = source_recommend,source_love = source_love,data = detail,come = come,source = result,num = num)
    except:
        return render_template("zi_yuan/zi_yuan_detail.html", source_recommend=source_recommend,
                               source_love=source_love, data=detail, come=come, source=result, num=num)
#资源comment读取
@app.route('/source_comment/<detail_id>')
def source_comment(detail_id):
    data = pysql.source_comment_read(detail_id)
    data_table_main = []
    for i, foo in enumerate(data):
        user_data = pysql.user_read(foo.user_id)
        target_user_name = pysql.user_name(foo.target_user_id)
        d = {}
        d['main'] = u'<div class="media">' \
                        '<div class="media-body">' \
                            '<a href="/user/'+str(foo.user_id)+'"><img src="' + url_for('static', filename='public/img/user/' + str(foo.user_id))+ '.png!100-100"alt="' + user_data.user_name + '" class ="align-self-start mr-1 rounded-circle" style="width:20px;margin-top:-3px">' + user_data.user_name + '</a>' \
                            '<div class="lv"><span class="lv-1" style="background-color:'+user_data.color+'">Lv</span><span class="lv-2" style="background-color:'+user_data.color+'">'+str(user_data.level)+'</span></div><span class="badge">&emsp;发表于:' + foo.time.strftime('%Y-%m-%d') + '</span>' \
                            '<br><br>' \
                            '<p>回复<b style="color:#007bff"><a  href="/user/'+str(foo.target_user_id)+'">@'+target_user_name+':</a></b>' + str(foo.content) + '</p>' \
                            '<div class="col-lg-12"><a href id="'+str(foo.id)+'" onclick="modalData(this)" data-detail_id="'+str(foo.detail_id)+'" data-target_source_id="'+str(foo.target_source_id)+'" data-user_id="'+str(foo.user_id)+'" class="main-title-buttom" data-toggle="modal" data-target="#Modal"><svg style="margin:0 5px;top:2px" fill="currentColor" viewBox="0 0 24 24" width="16" height="16"><path d="M22.959 17.22c-1.686-3.552-5.128-8.062-11.636-8.65-.539-.053-1.376-.436-1.376-1.561V4.678c0-.521-.635-.915-1.116-.521L1.469 10.67a1.506 1.506 0 0 0-.1 2.08s6.99 6.818 7.443 7.114c.453.295 1.136.124 1.135-.501V17a1.525 1.525 0 0 1 1.532-1.466c1.186-.139 7.597-.077 10.33 2.396 0 0 .396.257.536.257.892 0 .614-.967.614-.967z" fill-rule="evenodd"></path></svg>回复</a>' \
                            '</div>' \
                        '</div>' \
                    '</div>'
        data_table_main.append(d)
    data_table_main = json.dumps(data_table_main, sort_keys=True, indent=4, separators=(',', ': '))
    if data_table_main == []:
        data_table_main = ''
    return data_table_main
#资源conmmen回复
@app.route('/source_conmment_response',methods=['POST'])
@login
def source_conmment_response():
    if request.method == 'POST':
        detail_id = request.form.get('detail_id')
        target_user_id = request.form.get('user_id')
        user_id = session.get('user_id')
        target_source_id = request.form.get('target_source_id')
        content = request.form.get('content')
        pysql.creat_source_comment(detail_id,user_id,target_user_id,target_source_id,content)
        return redirect('/ziYuanDetail/{0}/0/0'.format(target_source_id))
    return ''
#sourceLove
@app.route('/sourceLove/<source_id>',methods=['POST','GET'])
def sourceLove(source_id):
    user_id = session.get('user_id')
    if user_id:
        return pysql.source_love_creat(user_id,source_id)
    return ''
@app.route('/zi_yuan/time_tb')
def time_tb():
    data = pysql.time_tb()
    if data:
        data_time = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    else:
        data_time = []
        data = []
    return render_template("zi_yuan/time_tb.html",data = data,data_time = data_time)
#fen_lei
@app.route('/zi_yuan/fen_lei')
def fen_lei():
    data = pysql.fen_lei()
    return render_template("zi_yuan/fen_lei.html",data = data)
import py.mv_jie_xi as pm
@app.route('/mv/api',methods=['GET'])
def mv_api():
    type = request.values.get('type')
    uid = request.values.get('uid')[0:-4]
    result = pm.mv(uid,type)
    if result:
        resp = make_response('mengkaby')
        resp.status = "302 Found"
        resp.headers['Location'] = result
        resp.headers['Content-Type'] = 'application/octet-stream'
        return resp
    else:
        return 'None'
@app.route('/mv',methods=['GET'])
def mv():
    yhdm_iframe = {
        'youku':'https://player.baodai.org/ipsign/player.php?v={}_youku',
        'bilibili':'https://player.baodai.org/ipsign/player.php?v={}&type=bilicid',
        'bilicid': 'https://player.baodai.org/ipsign/player.php?v={}&type=bilicid',
        'qq':'https://hh.tt-hk.cn/jx.php?url=https://v.qq.com/x/page/{}.html',
        'qiyi':'https://player.yaogougou.com/ipsign/player.php?id={}&type=iqiyi',
        'pptv':'https://player.yaogougou.com/ipsign/player.php?id={}&type=pptv',
        'vip':'https://player.yaogougou.com/ipsign/player.php?id={}&type=vip',
        'qqy':'https://player.yaogougou.com/ipsign/player.php?id=http://www.iqiyi.com/v_{}.html&type=vip',
        'tudou': 'https://api.flvsp.com/?type=tudou&vid={}',
        'pvod': 'https://api.flvsp.com/?type=letv&vid={}',
        'sohu':'https://api.flvsp.com/?type=sohu&vid={}',
        'acfun':'https://api.flvsp.com/?type=acfun&vid={}'
    }
    qqdm_iframe = {
        'sinahd':'http://99hd.net/mp4/ckplayer.html?id={}&type=sina',
        'pptv':'https://player.s1905.com/ipsign/player.php?v={}_pptv',
        'sohu':'https://player.s1905.com/ipsign/player.php?v={}_mysohu',
        'yuku':'https://player.s1905.com/ipsign/player.php?v={}_youku'
    }

    if request.method == 'GET':
        type = request.values.get('type')
        security = 1
        if type in ['sohu']:
            security = 0
        uid = request.values.get('uid')
        source_id = request.values.get('source_id')
        come = request.values.get('come')
        num = request.values.get('num')
        if str(come) < '3':
            if type in yhdm_iframe:
                return render_template('mv/iframe.html', url = yhdm_iframe[type].format(uid),security = security)
        else:
            if type in qqdm_iframe:
                return render_template('mv/iframe.html', url = qqdm_iframe[type].format(uid),security = security)
        return render_template('mv/deplayer.html',type = type,uid = uid,cur = '{}_{}'.format(source_id,num))
    return 'None'
if __name__ == '__main__':
    app.run(debug=True)
