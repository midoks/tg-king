# coding:utf-8

import sys
import io
import os
import time
import re
import json
import base64

sys.path.append(os.getcwd() + "/class/core")
import tgking

app_debug = False
if tgking.isAppleSystem():
    app_debug = True


def getModName():
    return 'admgr'


def getModDir():
    return tgking.getModDir() + '/' + getModName()


def getServerDir():
    return tgking.getServerDir() + '/' + getModName()


def getInitDFile():
    if app_debug:
        return '/tmp/' + getModName()
    return '/etc/init.d/' + getModName()


def getInitDTpl():
    path = getModDir() + "/init.d/" + getModName() + ".tpl"
    return path


def initDreplace():

    file_tpl = getInitDTpl()
    app_path = service_path + '/' + getModName()

    initD_path = getServerDir() + '/init.d'
    if not os.path.exists(initD_path):
        os.mkdir(initD_path)
    file_bin = initD_path + '/' + getModName()

    content = tgking.readFile(file_tpl)
    content = content.replace('{$SERVER_PATH}', service_path + '/mdserver-web')
    content = content.replace('{$APP_PATH}', app_path)

    tgking.writeFile(file_bin, content)
    tgking.execShell('chmod +x ' + file_bin)

    # systemd
    systemDir = tgking.systemdCfgDir()
    systemService = systemDir + '/' + getModName() + '.service'
    systemServiceTpl = getPluginDir() + '/init.d/' + getModName() + '.service.tpl'
    if os.path.exists(systemDir) and not os.path.exists(systemService):
        service_path = tgking.getServerDir()
        se_content = tgking.readFile(systemServiceTpl)
        se_content = se_content.replace('{$APP_PATH}', app_path)
        tgking.writeFile(systemService, se_content)
        tgking.execShell('systemctl daemon-reload')

    return file_bin


def agOp(method):
    file = initDreplace()

    if not mw.isAppleSystem():
        data = mw.execShell('systemctl ' + method + ' ' + getPluginName())
        if data[1] == '':
            return 'ok'
        return data[1]

    data = mw.execShell(file + ' ' + method)
    # print(data)
    if data[1] == '':
        return 'ok'
    return 'ok'


def start():
    return agOp('start')


def stop():
    return agOp('stop')


def restart():
    status = agOp('restart')
    return status


def reload():
    return agOp('restart')


def status():
    data = tgking.execShell(
        "ps -ef | grep admgr_bot |grep -v grep | awk '{print $2}'")
    if data[0] == '':
        return 'stop'
    return 'start'


def initdStatus():
    if tgking.isAppleSystem():
        return "Apple Computer does not support"

    shell_cmd = 'systemctl status ' + \
        getPluginName() + ' | grep loaded | grep "enabled;"'
    data = tgking.execShell(shell_cmd)
    if data[0] == '':
        return 'fail'
    return 'ok'


def initdInstall():
    if tgking.isAppleSystem():
        return "Apple Computer does not support"

    tgking.execShell('systemctl enable ' + getPluginName())
    return 'ok'


def initdUinstall():
    if tgking.isAppleSystem():
        return "Apple Computer does not support"

    tgking.execShell('systemctl disable ' + getPluginName())
    return 'ok'


def runLog():
    p = getServerDir() + '/task.log'
    return p

if __name__ == "__main__":
    func = sys.argv[1]
    if func == 'status':
        print(status())
    elif func == 'start':
        print(start())
    elif func == 'stop':
        print(stop())
    elif func == 'restart':
        print(restart())
    elif func == 'reload':
        print(reload())
    elif func == 'initd_status':
        print(initdStatus())
    elif func == 'initd_install':
        print(initdInstall())
    elif func == 'initd_uninstall':
        print(initdUinstall())
    elif func == 'run_log':
        print(runLog())
    else:
        print('error')
