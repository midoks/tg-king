# coding:utf-8

import sys
import io
import os
import time
import shutil
import uuid
import json
import traceback
import socket

# reload(sys)
#  sys.setdefaultencoding('utf-8')
import paramiko
from datetime import timedelta

from flask import Flask
from flask import render_template
from flask import make_response
from flask import Response
from flask import session
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template_string, abort
from flask_caching import Cache
from flask_session import Session


from whitenoise import WhiteNoise

sys.path.append(os.getcwd() + "/class/core")

import config
import tgking

app = Flask(__name__, template_folder='templates/default')
app.config.version = config.config().getVersion()

app.wsgi_app = WhiteNoise(
    app.wsgi_app, root="route/static/", prefix="static/", max_age=604800)

cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app, config={'CACHE_TYPE': 'simple'})

try:
    from flask_sqlalchemy import SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/tgking_session.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['SESSION_SQLALCHEMY'] = sdb
    app.config['SESSION_SQLALCHEMY_TABLE'] = 'session'
    sdb = SQLAlchemy(app)
    sdb.create_all()
except:
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = '/tmp/py_tgking_session_' + \
        str(sys.version_info[0])
    app.config['SESSION_FILE_THRESHOLD'] = 1024
    app.config['SESSION_FILE_MODE'] = 384

app.secret_key = uuid.UUID(int=uuid.getnode()).hex[-12:]
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'MW_:'
app.config['SESSION_COOKIE_NAME'] = "MW_VER_1"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)


app.config['DEBUG'] = True


# socketio
from flask_socketio import SocketIO, emit, send
socketio = SocketIO()
socketio.init_app(app)

# sockets
from flask_sockets import Sockets
sockets = Sockets(app)

# from gevent.pywsgi import WSGIServer
# from geventwebsocket.handler import WebSocketHandler
# http_server = WSGIServer(('0.0.0.0', '7200'), app,
#                          handler_class=WebSocketHandler)
# http_server.serve_forever()

# debug macosx dev
if tgking.isDebugMode():
    app.debug = True
    app.config.version = app.config.version + str(time.time())

app.debug = True
app.config.version = app.config.version + str(time.time())

import common
common.init()


# # ----------  error function start -----------------
# def getErrorNum(key, limit=None):
#     key = tgking.md5(key)
#     num = cache.get(key)
#     if not num:
#         num = 0
#     if not limit:
#         return num
#     if limit > num:
#         return True
#     return False


# def setErrorNum(key, empty=False, expire=3600):
#     key = tgking.md5(key)
#     num = cache.get(key)
#     if not num:
#         num = 0
#     else:
#         if empty:
#             cache.delete(key)
#             return True
#     cache.set(key, num + 1, expire)
#     return True
# # ----------  error function end -----------------


def isLogined():
    return True
    if 'login' in session and 'username' in session and session['login'] == True:
        userInfo = tgking.M('users').where(
            "id=?", (1,)).field('id,username,password').find()
        # print(userInfo)
        if userInfo['username'] != session['username']:
            return False

        now_time = int(time.time())

        if 'overdue' in session and now_time > session['overdue']:
            # 自动续期
            session['overdue'] = int(time.time()) + 7 * 24 * 60 * 60
            return False

        if 'tmp_login_expire' in session and now_time > int(session['tmp_login_expire']):
            session.clear()
            return False

        return True

    return False


def publicObject(toObject, func, action=None, get=None):
    name = tgking.toSmallHump(func) + 'Api'
    # print(toObject,name)
    try:
        if hasattr(toObject, name):
            efunc = 'toObject.' + name + '()'
            data = eval(efunc)
            return data
        data = {'msg': '404,not find api[' + name + ']', "status": False}
        return tgking.getJson(data)
    except Exception as e:
        if tgking.isDebugMode():
            print(traceback.print_exc())
        data = {'msg': '访问异常:' + str(e) + '!', "status": False}
        return tgking.getJson(data)


# @app.route('/close')
# def close():
#     if not os.path.exists('data/close.pl'):
#         return redirect('/')
#     data = {}
#     data['cmd'] = 'rm -rf ' + tgking.getRunDir() + '/data/close.pl'
#     return render_template('close.html', data=data)


# @app.route("/code")
# def code():
#     import vilidate
#     vie = vilidate.vieCode()
#     codeImage = vie.GetCodeImage(80, 4)
#     # try:
#     #     from cStringIO import StringIO
#     # except:
#     #     from StringIO import StringIO

#     out = io.BytesIO()
#     codeImage[0].save(out, "png")

#     # print(codeImage[1])

#     session['code'] = tgking.md5(''.join(codeImage[1]).lower())

#     img = Response(out.getvalue(), headers={'Content-Type': 'image/png'})
#     return make_response(img)


# @app.route("/check_login", methods=['POST'])
# def checkLogin():
#     if isLogined():
#         return "true"
#     return "false"


# @app.route("/do_login", methods=['POST'])
# def doLogin():
#     login_cache_count = 5
#     login_cache_limit = cache.get('login_cache_limit')

#     filename = 'data/close.pl'
#     if os.path.exists(filename):
#         return tgking.returnJson(False, '面板已经关闭!')

#     username = request.form.get('username', '').strip()
#     password = request.form.get('password', '').strip()
#     code = request.form.get('code', '').strip()
#     # print(session)
#     if 'code' in session:
#         if session['code'] != tgking.md5(code):
#             if login_cache_limit == None:
#                 login_cache_limit = 1
#             else:
#                 login_cache_limit = int(login_cache_limit) + 1

#             if login_cache_limit >= login_cache_count:
#                 tgking.writeFile(filename, 'True')
#                 return tgking.returnJson(False, '面板已经关闭!')

#             cache.set('login_cache_limit', login_cache_limit, timeout=10000)
#             login_cache_limit = cache.get('login_cache_limit')
#             code_msg = tgking.getInfo("验证码错误,您还可以尝试[{1}]次!", (str(
#                 login_cache_count - login_cache_limit)))
#             tgking.writeLog('用户登录', code_msg)
#             return tgking.returnJson(False, code_msg)

#     userInfo = tgking.M('users').where(
#         "id=?", (1,)).field('id,username,password').find()

#     # print(userInfo)
#     # print(password)
#     password = tgking.md5(password)
#     # print('md5-pass', password)

#     if userInfo['username'] != username or userInfo['password'] != password:
#         msg = "<a style='color: red'>密码错误</a>,帐号:{1},密码:{2},登录IP:{3}", ((
#             '****', '******', request.remote_addr))

#         if login_cache_limit == None:
#             login_cache_limit = 1
#         else:
#             login_cache_limit = int(login_cache_limit) + 1

#         if login_cache_limit >= login_cache_count:
#             tgking.writeFile(filename, 'True')
#             return tgking.returnJson(False, '面板已经关闭!')

#         cache.set('login_cache_limit', login_cache_limit, timeout=10000)
#         login_cache_limit = cache.get('login_cache_limit')
#         tgking.writeLog('用户登录', tgking.getInfo(msg))
# return tgking.returnJson(False, tgking.getInfo("用户名或密码错误,您还可以尝试[{1}]次!",
# (str(login_cache_count - login_cache_limit))))

#     cache.delete('login_cache_limit')
#     session['login'] = True
#     session['username'] = userInfo['username']
#     session['overdue'] = int(time.time()) + 7 * 24 * 60 * 60
#     # session['overdue'] = int(time.time()) + 7

#     # fix 跳转时,数据消失，可能是跨域问题
#     # tgking.writeFile('data/api_login.txt', userInfo['username'])
#     return tgking.returnJson(True, '登录成功,正在跳转...')


@app.errorhandler(404)
def page_unauthorized(error):
    return render_template_string('404 not found', error_info=error), 404


def return_safe_path(path, req, data, pageFile):
    if path != req and not isLogined():
        if data['status_code'] == '0':
            return render_template('path.html')
        else:
            return Response(status=int(data['status_code']))

    if not isLogined():
        return render_template('login.html', data=data)

    if not req in pageFile:
        return redirect('/')

    return render_template(req + '.html', data=data)


@app.route('/<reqClass>/<reqAction>', methods=['POST', 'GET'])
@app.route('/<reqClass>/', methods=['POST', 'GET'])
@app.route('/<reqClass>', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def index(reqClass=None, reqAction=None, reqData=None):

    comReturn = common.local()
    if comReturn:
        return comReturn

    # 页面请求
    if reqAction == None:
        import config
        data = config.config().get()

        if reqClass == None:
            reqClass = 'index'

        page_file = ('index', 'user', 'bot', 'client', 'login', 'module')

        # 设置了安全路径
        safe_pathinfo = tgking.getSafePath()

        if safe_pathinfo[0]:
            return return_safe_path(safe_pathinfo[1], reqClass, data, page_file)

        # 登录页
        if reqClass == 'login':

            signout = request.args.get('signout', '')
            if signout == 'True':
                session.clear()
                session['login'] = False
                session['overdue'] = 0

            if safe_pathinfo[0]:
                return return_safe_path(safe_pathinfo[1], reqClass, data, page_file)

            return render_template('login.html', data=data)

        if not reqClass in page_file:
            return redirect('/')

        # if not isLogined():
        #     return redirect('/login')

        return render_template(reqClass + '.html', data=data)

    # if not isLogined():
    #     return 'error request!'

    # API请求
    classFile = ('tgbot_api', 'tgclient_api')
    className = reqClass + '_api'
    if not className in classFile:
        return "api error request"

    eval_str = "__import__('" + className + "')." + className + '()'
    newInstance = eval(eval_str)

    return publicObject(newInstance, reqAction)
