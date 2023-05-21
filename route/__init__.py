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
app.config['SESSION_KEY_PREFIX'] = 'TGClient:'
app.config['SESSION_COOKIE_NAME'] = "TGClient_VER_1"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)

app.config['DEBUG'] = True

# socketio
from flask_socketio import SocketIO, emit, send
socketio = SocketIO()
socketio.init_app(app)

# sockets
from flask_sockets import Sockets
sockets = Sockets(app)

# debug macosx dev
if tgking.isDebugMode():
    app.debug = True
    app.config.version = app.config.version + str(time.time())

import common
common.init()


def isLogined():
    # print('isLogined', session)
    if 'login' in session and 'username' in session and session['login'] == True:
        userInfo = tgking.M('users').where(
            "id=?", (1,)).field('id,username,password').find()
        if userInfo['username'] != session['username']:
            return False

        now_time = int(time.time())
        if 'overdue' in session and now_time > session['overdue']:
            # 自动续期
            session['overdue'] = int(time.time()) + 7 * 24 * 60 * 60
            return False
        return True
    return False


def publicObject(toObject, func, action=None, get=None):
    name = tgking.toSmallHump(func) + 'Api'
    print(toObject, name)
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


@app.route("/do_login", methods=['POST'])
def doLogin():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    password = tgking.md5(password)

    userInfo = tgking.M('users').where(
        "id=?", (1,)).field('id,username,password').find()

    if userInfo['username'] != username or userInfo['password'] != password:
        msg = "<a style='color: red'>密码错误</a>,登录IP:" + request.remote_addr
        return tgking.returnCode(-1, msg)

    session['login'] = True
    session['username'] = userInfo['username']
    session['overdue'] = int(time.time()) + 7 * 24 * 60 * 60
    return tgking.returnCode(0, '登录成功,正在跳转...')


@app.errorhandler(404)
def page_unauthorized(error):
    return render_template_string('404 not found', error_info=error), 404


def return_safe_path(path, req, data, pageFile):
    if path != req and not isLogined():
        if str(data['status_code']) == '0':
            return render_template('path.html', data=data)
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

        page_file = ('index', 'bot', 'client', 'logs',
                     'config', 'login', 'module')

        # 设置了安全路径
        safe_pathinfo = tgking.getSafePath()

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

        if safe_pathinfo[0]:
            return return_safe_path(safe_pathinfo[1], reqClass, data, page_file)

        if not reqClass in page_file:
            return redirect('/')

        if not isLogined():
            return redirect('/login')

        return render_template(reqClass + '.html', data=data)

    if not isLogined():
        return tgking.returnCode(-1, 'error request!')

    # API请求
    classFile = ('module_api', 'tgbot_api', 'tgclient_api', 'logs_api')
    className = reqClass + '_api'
    if not className in classFile:
        return tgking.returnCode(-1, 'api error request!')

    eval_str = "__import__('" + className + "')." + className + '()'
    newInstance = eval(eval_str)

    return publicObject(newInstance, reqAction)
