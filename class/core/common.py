# coding:utf-8

# ---------------------------------------------------------------------------------
# TG全能王面板
# ---------------------------------------------------------------------------------
# copyright (c) 2023-∞(https://github.com/midoks/tg-king) All rights reserved.
# ---------------------------------------------------------------------------------
# Author: midoks <midoks@163.com>
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
# 配置操作
# ---------------------------------------------------------------------------------

import os
import db

import tgking


def init():
    initDB()
    initInitD()


def initDB():
    try:
        sql = db.Sql().dbfile('default')
        csql = readFile('data/sql/default.sql')
        csql_list = csql.split(';')
        for index in range(len(csql_list)):
            sql.execute(csql_list[index], ())

    except Exception as ex:
        print(str(ex))


def initInitD():
    script = tgking.getRunDir() + '/scripts/init.d/tgking.tpl'
    script_bin = tgking.getRunDir() + '/scripts/init.d/tgking'
    doContentReplace(script, script_bin)
    tgking.execShell('chmod +x ' + script_bin)

    # 在linux系统中,确保/etc/init.d存在
    if not tgking.isAppleSystem() and not os.path.exists("/etc/rc.d/init.d"):
        tgking.execShell('mkdir -p /etc/rc.d/init.d')

    if not tgking.isAppleSystem() and not os.path.exists("/etc/init.d"):
        tgking.execShell('mkdir -p /etc/init.d')

    # initd
    if os.path.exists('/etc/rc.d/init.d'):
        initd_bin = '/etc/rc.d/init.d/tgking'
        if not os.path.exists(initd_bin):
            import shutil
            shutil.copyfile(script_bin, initd_bin)
            tgking.execShell('chmod +x ' + initd_bin)
        # 加入自启动
        tgking.execShell('which chkconfig && chkconfig --add tgking')

    if os.path.exists('/etc/init.d'):
        initd_bin = '/etc/init.d/tgking'
        if not os.path.exists(initd_bin):
            import shutil
            shutil.copyfile(script_bin, initd_bin)
            tgking.execShell('chmod +x ' + initd_bin)
        # 加入自启动
        tgking.execShell('which update-rc.d && update-rc.d -f tgking defaults')

    # 获取系统IPV4
    tgking.setHostAddr(tgking.getLocalIp())


def local():
    result = checkClose()
    if result:
        return result


# 检查面板是否关闭
def checkClose():
    if os.path.exists('data/close.pl'):
        return redirect('/close')


def doContentReplace(src, dst):
    content = tgking.readFile(src)
    content = content.replace("{$SERVER_PATH}", tgking.getRunDir())
    tgking.writeFile(dst, content)
