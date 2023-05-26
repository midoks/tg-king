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
    err = traceback.format_exc()
    return err


def getRunDir():
    return os.getcwd()


def getRootDir():
    return os.path.dirname(getRunDir())


def getServerDir():
    return getRootDir() + '/tg-king'


def getModDir():
    return getServerDir() + '/module'


def getPathSuffix(path):
    return os.path.splitext(path)[-1]


def readFile(filename):
    # 读文件内容
    try:
        fp = open(filename, 'r')
        fBody = fp.read()
        fp.close()
        return fBody
    except Exception as e:
        print(getTracebackInfo())
        return False


def readBinFile(filename):
    # 读文件内容
    try:
        fp = open(filename, 'rb')
        fBody = fp.read()
        fp.close()
        return fBody
    except Exception as e:
        print(getTracebackInfo())
        return False


def writeBinFile(filename, content):
    # 写文件内容
    try:
        fp = open(filename, 'wb+')
        fp.write(content)
        fp.close()
        return True
    except Exception as e:
        print(getTracebackInfo())
        return False


def writeFile(filename, content, mode='w+'):
    # 写文件内容
    try:
        fp = open(filename, mode)
        fp.write(content)
        fp.close()
        return True
    except Exception as e:
        print(getTracebackInfo())
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


def getRandomString(length):
    # 取随机字符串
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    chrlen = len(chars) - 1
    random = Random()
    for i in range(length):
        str += chars[random.randint(0, chrlen)]
    return str


def getUniqueId():
    """
    根据时间生成唯一ID
    :return:
    """
    current_time = datetime.datetime.now()
    str_time = current_time.strftime('%Y%m%d%H%M%S%f')[:-3]
    unique_id = "{0}".format(str_time)
    return unique_id


def isDebugMode():
    if isAppleSystem():
        return True

    debugPath = getRunDir() + "/data/debug.pl"
    if os.path.exists(debugPath):
        return True

    return False


def M(table):
    sql = db.Sql()
    return sql.table(table)


def toSmallHump(name):
    block = name.split('_')
    name = block[0]
    for x in range(len(block) - 1):
        suf = block[x + 1].title()
        name += suf
    return name


def md5(content):
    # 生成MD5
    try:
        m = hashlib.md5()
        m.update(content.encode("utf-8"))
        return m.hexdigest()
    except Exception as ex:
        return False


def getFileMd5(filename):
    # 文件的MD5值
    if not os.path.isfile(filename):
        return False

    myhash = hashlib.md5()
    f = file(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()


def systemdCfgDir():
    # ubuntu
    cfg_dir = '/lib/systemd/system'
    if os.path.exists(cfg_dir):
        return cfg_dir

    # debian,centos
    cfg_dir = '/usr/lib/systemd/system'
    if os.path.exists(cfg_dir):
        return cfg_dir

    # local test
    return "/tmp"


def modLog(stype, msg):
    return writeDbLog('模块日志[' + stype + ']', msg)


def writeDbLog(stype, msg, args=(), uid=1):
    try:
        import time
        import db
        import json
        sql = db.Sql()
        mdate = time.strftime('%Y-%m-%d %X', time.localtime())
        wmsg = getInfo(msg, args)
        data = (stype, wmsg, uid, mdate)
        result = sql.table('logs').add('type,log,uid,addtime', data)
        return True
    except Exception as e:
        return False


def writeModLog(log_str, module_name='tmp'):
    if __name__ == "__main__":
        print(log_str)

    now = getDateFromNow()
    log_file = getServerDir() + '/logs/module_' + module_name + '.log'
    writeLog(now + ':' + log_str, log_file, limit_size=5 * 1024)
    return True


def writeLog(msg, path=None, limit_size=50 * 1024 * 1024, save_limit=3):
    log_file = getServerDir() + '/logs/debug.log'
    if path != None:
        log_file = path

    if os.path.exists(log_file):
        size = os.path.getsize(log_file)
        if size > limit_size:
            log_file_rename = log_file + "_" + \
                time.strftime("%Y-%m-%d_%H%M%S") + '.log'
            os.rename(log_file, log_file_rename)
            logs = sorted(glob.glob(log_file + "_*"))
            count = len(logs)
            save_limit = count - save_limit
            for i in range(count):
                if i > save_limit:
                    break
                os.remove(logs[i])
                # print('|---多余日志[' + logs[i] + ']已删除!')

    f = open(log_file, 'ab+')
    msg += "\n"
    if __name__ == '__main__':
        print(msg)
    f.write(msg.encode('utf-8'))
    f.close()
    return True


def getJson(data):
    import json
    return json.dumps(data)


def returnData(status, msg, data=None):
    return {'status': status, 'msg': msg, 'data': data}


def returnJson(status, msg, data=None):
    if data == None:
        return getJson({'status': status, 'msg': msg})
    return getJson({'status': status, 'msg': msg, 'data': data})


def returnCode(code, msg, data=None):
    if data == None:
        return getJson({'code': code, 'msg': msg})
    return getJson({'code': code, 'msg': msg, 'data': data})


def getSafePath():
    path = 'data/admin_path.pl'
    if os.path.exists(path):
        cont = readFile(path)
        cont = cont.strip().strip('/')
        return (True, cont)
    return (False, '')


def getLastLine(path, num, p=1):
    pyVersion = sys.version_info[0]
    try:
        import html
        if not os.path.exists(path):
            return ""
        start_line = (p - 1) * num
        count = start_line + num
        fp = open(path, 'rb')
        buf = ""

        fp.seek(0, 2)
        if fp.read(1) == "\n":
            fp.seek(0, 2)
        data = []
        b = True
        n = 0

        for i in range(count):
            while True:
                newline_pos = str.rfind(str(buf), "\n")
                pos = fp.tell()
                if newline_pos != -1:
                    if n >= start_line:
                        line = buf[newline_pos + 1:]
                        try:
                            data.insert(0, html.escape(line))
                        except Exception as e:
                            pass
                    buf = buf[:newline_pos]
                    n += 1
                    break
                else:
                    if pos == 0:
                        b = False
                        break
                    to_read = min(4096, pos)
                    fp.seek(-to_read, 1)
                    t_buf = fp.read(to_read)
                    if pyVersion == 3:
                        if type(t_buf) == bytes:
                            t_buf = t_buf.decode("utf-8", "ignore").strip()
                    buf = t_buf + buf
                    fp.seek(-to_read, 1)
                    if pos - to_read == 0:
                        buf = "\n" + buf
            if not b:
                break
        fp.close()
    except Exception as e:
        return str(e)

    return "\n".join(data)


def getDate():
    # 取格式时间
    import time
    return time.strftime('%Y-%m-%d %X', time.localtime())


def getDateFromNow(tf_format="%Y-%m-%d %H:%M:%S", time_zone="Asia/Shanghai"):
    # 取格式时间
    import time
    os.environ['TZ'] = time_zone
    time.tzset()
    return time.strftime(tf_format, time.localtime())


def getDataFromInt(val):
    time_format = '%Y-%m-%d %H:%M:%S'
    time_str = time.localtime(val)
    return time.strftime(time_format, time_str)


def getBotRangeList(module_name):
    data = M('module').field('id,status,range_type,range_val_bot').where(
        'name=?', (module_name,)).select()

    # print(data[0]['range_type'])
    if data[0]['range_type'] == 0:
        return M('tg_bot').field('id,alias,token').select()

    if data[0]['range_type'] == 1:
        return M('tg_bot').field('id,alias,token').where('id in (?)', (data[0]['range_val_bot'],)).select()

    if data[0]['range_type'] == 2:
        return M('tg_bot').field('id,alias,token').where('id not in (?)', (data[0]['range_val_bot'],)).select()

    return []


def getBotById(tid):
    t = M('tg_bot').field('id,alias,token').where('id=?', (tid,)).select()
    if len(t) > 0:
        return t[0]
    else:
        return {}


def getClientRangeList(module_name):
    data = M('module').field('id,status,range_type,range_val_client').where(
        'name=?', (module_name,)).select()

    if data[0]['range_type'] == 0:
        return M('tg_client').field('id,app_id,app_hash').select()

    if data[0]['range_type'] == 1:
        return M('tg_client').field('id,app_id,app_hash').where('id in (?)', (data[0]['range_val_client'],)).select()

    if data[0]['range_type'] == 2:
        return M('tg_client').field('id,app_id,app_hash').where('id not in (?)', (data[0]['range_val_client'],)).select()
    return []


def getClientById(tid):
    t = M('tg_client').field('id,app_id,app_hash,is_vaild,data').where(
        'id=?', (tid,)).select()
    if len(t) > 0:
        return t[0]
    else:
        return {}
