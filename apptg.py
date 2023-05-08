# coding:utf-8

# ---------------------------------------------------------------------------------
# TG全能王面板
# ---------------------------------------------------------------------------------
# copyright (c) 2023-∞(https://github.com/midoks/tg-king) All rights reserved.
# ---------------------------------------------------------------------------------
# Author: midoks <midoks@163.com>
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
# 入口文件
# ---------------------------------------------------------------------------------

import sys
import io
import os

sys.dont_write_bytecode = True
from route import app, socketio


from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

from gevent import monkey
monkey.patch_all()

try:
    if __name__ == "__main__":

        PORT = 1314
        if os.path.exists('data/port.pl'):
            f = open('data/port.pl')
            PORT = int(f.read())
            f.close()

        http_server = WSGIServer(
            (HOST, PORT), app, handler_class=WebSocketHandler)
        http_server.serve_forever()
        socketio.run(app, host=HOST, port=PORT)
except Exception as ex:
    print(ex)
