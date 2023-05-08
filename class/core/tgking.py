# coding:utf-8

# ---------------------------------------------------------------------------------
# TG全能王面板
# ---------------------------------------------------------------------------------
# copyright (c) 2023-∞(https://github.com/midoks/tg-king) All rights reserved.
# ---------------------------------------------------------------------------------
# Author: midoks <midoks@163.com>
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
# 核心方法
# ---------------------------------------------------------------------------------

import os
import sys
import time
import string
import json
import hashlib
import shlex
import datetime
import subprocess
import glob
import base64
import re

from random import Random

import db


def execShell(cmdstring, cwd=None, timeout=None, shell=True):

    if shell:
        cmdstring_list = cmdstring
    else:
        cmdstring_list = shlex.split(cmdstring)
    if timeout:
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

    sub = subprocess.Popen(cmdstring_list, cwd=cwd, stdin=subprocess.PIPE,
                           shell=shell, bufsize=4096, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while sub.poll() is None:
        time.sleep(0.1)
        if timeout:
            if end_time <= datetime.datetime.now():
                raise Exception("Timeout：%s" % cmdstring)

    if sys.version_info[0] == 2:
        return sub.communicate()

    data = sub.communicate()
    # python3 fix 返回byte数据
    if isinstance(data[0], bytes):
        t1 = str(data[0], encoding='utf-8')

    if isinstance(data[1], bytes):
        t2 = str(data[1], encoding='utf-8')
    return (t1, t2)


def getOs():
    return sys.platform


def isAppleSystem():
    if getOs() == 'darwin':
        return True
    return False


def getTracebackInfo():
    import traceback
    errorMsg = traceback.format_exc()
    return errorMsg


def getRunDir():
    return os.getcwd()


def getRootDir():
    return os.path.dirname(os.path.dirname(getRunDir()))


def readFile(filename):
    # 读文件内容
    try:
        fp = open(filename, 'r')
        fBody = fp.read()
        fp.close()
        return fBody
    except Exception as e:
        # print(e)
        return False


def writeFile(filename, content, mode='w+'):
    # 写文件内容
    try:
        fp = open(filename, mode)
        fp.write(content)
        fp.close()
        return True
    except Exception as e:
        return False


def getLocalIp():
    filename = 'data/iplist.txt'
    try:
        ipaddress = readFile(filename)
        if not ipaddress or ipaddress == '127.0.0.1':
            cmd = "curl --insecure -4 -sS --connect-timeout 5 -m 60 https://v6r.ipip.net/?format=text"
            ip = execShell(cmd)
            result = ip[0].strip()
            if result == '':
                raise Exception("ipv4 is empty!")
            writeFile(filename, result)
            return result
        return ipaddress
    except Exception as e:
        cmd = "curl --insecure -6 -sS --connect-timeout 5 -m 60 https://v6r.ipip.net/?format=text"
        ip = execShell(cmd)
        result = ip[0].strip()
        if result == '':
            return '127.0.0.1'
        writeFile(filename, result)
        return result
    finally:
        pass
    return '127.0.0.1'


def setHostAddr(addr):
    file = getRunDir() + '/data/iplist.txt'
    return writeFile(file, addr)
