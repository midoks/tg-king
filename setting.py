# coding:utf-8

# ---------------------------------------------------------------------------------
# TG全能王面板
# ---------------------------------------------------------------------------------
# copyright (c) 2023-∞(https://github.com/midoks/tg-king) All rights reserved.
# ---------------------------------------------------------------------------------
# Author: midoks <midoks@163.com>
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
# 配置文件
# ---------------------------------------------------------------------------------


import time
import sys
import random
import os

pwd = os.getcwd()
sys.path.append(pwd + '/class/core')

import tgking

log_dir = os.getcwd() + '/logs'
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

# default port
tgking_port = "1314"
if os.path.exists("data/port.pl"):
    tgking_port = tgking.readFile('data/port.pl')
    tgking_port.strip()
else:
    import common
    common.initDB()
    tgking_port = str(random.randint(10000, 65530))
    tgking.writeFile('data/port.pl', tgking_port)

bind = []
if os.path.exists('data/ipv6.pl'):
    bind.append('[0:0:0:0:0:0:0:0]:%s' % tgking_port)
else:
    bind.append('0.0.0.0:%s' % tgking_port)

threads = 1
backlog = 512
reload = False
daemon = True
worker_class = 'geventwebsocket.gunicorn.workers.GeventWebSocketWorker'
timeout = 7200
keepalive = 60
preload_app = True
capture_output = True
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
loglevel = 'info'
errorlog = log_dir + '/error.log'
accesslog = log_dir + '/access.log'
pidfile = log_dir + '/tgking.pid'
