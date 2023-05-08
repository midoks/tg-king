# coding:utf-8

# ---------------------------------------------------------------------------------
# TG全能王面板
# ---------------------------------------------------------------------------------
# copyright (c) 2023-∞(https://github.com/midoks/tg-king) All rights reserved.
# ---------------------------------------------------------------------------------
# Author: midoks <midoks@163.com>
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
# 工具箱
# ---------------------------------------------------------------------------------


import sys
import os
import json
import time
import re

sys.path.append(os.getcwd() + "/class/core")
import tgking
import db

INIT_DIR = "/etc/rc.d/init.d"
if tgking.isAppleSystem():
    INIT_DIR = tgking.getRunDir() + "/scripts/init.d"

INIT_CMD = INIT_DIR + "/tgking"


def tgking_input_cmd(msg):
    if sys.version_info[0] == 2:
        in_val = raw_input(msg)
    else:
        in_val = input(msg)
    return in_val


def tgking_cli(tgking_input=0):
    raw_tip = "======================================================"
    if not tgking_input:
        print("===============mdserver-web cli tools=================")
        print("(1)      重启面板服务")
        print("(2)      停止面板服务")
        print("(3)      启动面板服务")
        print("(4)      重载面板服务")
        print("(5)      修改面板端口")
        print("(10)     查看面板默认信息")
        print("(11)     修改面板密码")
        print("(12)     修改面板用户名")
        print("(13)     显示面板错误日志")
        print("(20)     关闭BasicAuth认证")
        print("(21)     解除域名绑定")
        print("(100)    开启PHP52显示")
        print("(101)    关闭PHP52显示")
        print("(200)    切换Linux系统软件源")
        print("(201)    简单速度测试")
        print("(0)      取消")
        print(raw_tip)
        try:
            tgking_input = input("请输入命令编号：")
            if sys.version_info[0] == 3:
                tgking_input = int(tgking_input)
        except:
            tgking_input = 0

    nums = [1, 2, 3, 4, 5, 10, 11, 12, 13, 20, 21, 100, 101, 200, 201]
    if not tgking_input in nums:
        print(raw_tip)
        print("已取消!")
        exit()

    if tgking_input == 1:
        os.system(INIT_CMD + " restart")
    elif tgking_input == 2:
        os.system(INIT_CMD + " stop")
    elif tgking_input == 3:
        os.system(INIT_CMD + " start")
    elif tgking_input == 4:
        os.system(INIT_CMD + " reload")
    elif tgking_input == 5:
        in_port = tgking_input_cmd("请输入新的面板端口：")
        in_port_int = int(in_port.strip())
        if in_port_int < 65536 and in_port_int > 0:
            import firewall_api
            firewall_api.firewall_api().addAcceptPortArgs(
                in_port, 'WEB面板[TOOLS修改]', 'port')
            tgking.writeFile('data/port.pl', in_port)
            os.system(INIT_CMD + " restart_panel")
            os.system(INIT_CMD + " default")
        else:
            print("|-端口范围在0-65536之间")
        return
    elif tgking_input == 10:
        os.system(INIT_CMD + " default")
    elif tgking_input == 11:
        input_pwd = tgking_input_cmd("请输入新的面板密码：")
        if len(input_pwd.strip()) < 5:
            print("|-错误，密码长度不能小于5位")
            return
        set_panel_pwd(input_pwd.strip(), True)
    elif tgking_input == 12:
        input_user = tgking_input_cmd("请输入新的面板用户名(>=5位)：")
        set_panel_username(input_user.strip())
    elif tgking_input == 13:
        os.system('tail -100 ' + tgking.getRunDir() + '/logs/error.log')
    elif tgking_input == 201:
        os.system('curl -Lso- bench.sh | bash')


def set_panel_pwd(password, ncli=False):
    # 设置面板密码
    import db
    sql = db.Sql()
    result = sql.table('users').where('id=?', (1,)).setField(
        'password', tgking.md5(password))
    username = sql.table('users').where('id=?', (1,)).getField('username')
    if ncli:
        print("|-用户名: " + username)
        print("|-新密码: " + password)
    else:
        print(username)


def show_panel_pwd():
    # 设置面板密码
    import db
    sql = db.Sql()
    password = sql.table('users').where('id=?', (1,)).getField('password')

    file_pwd = ''
    if os.path.exists('data/default.pl'):
        file_pwd = tgking.readFile('data/default.pl').strip()

    if tgking.md5(file_pwd) == password:
        print('password: ' + file_pwd)
        return
    print("password has been changed!")


def set_panel_username(username=None):
    # 随机面板用户名
    import db
    sql = db.Sql()
    if username:
        if len(username) < 5:
            print("|-错误，用户名长度不能少于5位")
            return
        if username in ['admin', 'root']:
            print("|-错误，不能使用过于简单的用户名")
            return

        sql.table('users').where('id=?', (1,)).setField('username', username)
        print("|-新用户名: %s" % username)
        return

    username = sql.table('users').where('id=?', (1,)).getField('username')
    if username == 'admin':
        username = tgking.getRandomString(8).lower()
        sql.table('users').where('id=?', (1,)).setField('username', username)
    print('username: ' + username)


def getServerIp():
    version = sys.argv[2]
    ip = tgking.execShell(
        "curl --insecure -{} -sS --connect-timeout 5 -m 60 https://v6r.ipip.net/?format=text".format(version))
    print(ip[0])


if __name__ == "__main__":
    method = sys.argv[1]
    if method == 'panel':
        set_panel_pwd(sys.argv[2])
    elif method == 'username':
        if len(sys.argv) > 2:
            set_panel_username(sys.argv[2])
        else:
            set_panel_username()
    elif method == 'password':
        show_panel_pwd()
    elif method == 'getServerIp':
        getServerIp()
    elif method == "cli":
        clinum = 0
        try:
            if len(sys.argv) > 2:
                clinum = int(sys.argv[2]) if sys.argv[2][:6] else sys.argv[2]
        except:
            clinum = sys.argv[2]
        tgking_cli(clinum)
    else:
        print('ERROR: Parameter error')