# coding:utf-8

# ---------------------------------------------------------------------------------
# TG全能王面板
# ---------------------------------------------------------------------------------
# copyright (c) 2023-∞(https://github.com/midoks/tg-king) All rights reserved.
# ---------------------------------------------------------------------------------
# Author: midoks <midoks@163.com>
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
# 模块操作
# ---------------------------------------------------------------------------------

import os
import json

import tgking

from flask import request


import threading


class module_api:

    __module_dir = 'module'

    def __init__(self):
        self.__module_dir = tgking.getRunDir() + '/module'

    def listApi(self):

        limit = request.form.get('limit', '10')
        page = request.form.get('page', '1')

        alist = self.getAllListPage('', int(page), int(limit))

        _ret = {}
        _ret['code'] = 0
        _ret['msg'] = 'ok'
        _ret['data'] = alist[0]
        _ret['count'] = alist[1]
        return tgking.getJson(_ret)

    def searchKey(self, info, kw):
        try:
            if info['title'].lower().find(kw) > -1:
                return True
            if info['ps'].lower().find(kw) > -1:
                return True
            if info['name'].lower().find(kw) > -1:
                return True
        except Exception as e:
            return False

    def getAllListPage(self, kw='', page=1, pageSize=10):
        module_info = []
        for dirinfo in os.listdir(self.__module_dir):
            if dirinfo[0:1] == '.':
                continue
            path = self.__module_dir + '/' + dirinfo
            if os.path.isdir(path):
                json_file = path + '/info.json'
                if os.path.exists(json_file):
                    try:
                        data = json.loads(tgking.readFile(json_file))
                        if kw != '' and not self.searchKey(data, kw):
                            continue
                        module_info.append(data)
                    except Exception as e:
                        print(tgking.getTracebackInfo())

        start = (page - 1) * pageSize
        end = start + pageSize
        _module_info = module_info[start:end]

        _module_info = self.checkModuleStatus(_module_info)
        return (_module_info, len(module_info))

    def checkModuleStatus(self, module_info):
        for i in range(len(module_info)):
            data = tgking.M('module').field('id,status').where(
                'name=?', (module_info[i]['name'],)).select()
            if len(data) == 0:
                module_info[i]['status'] = 'stop'
            else:
                module_info[i]['status'] = data[0]['status']
        return module_info

    def settingApi(self):
        module_name = request.args.get('module_name', '')
        # print(module_name)
        html = self.__module_dir + '/' + module_name + '/index.html'
        return tgking.readFile(html)

    def enableApi(self):
        module_name = request.form.get('module_name', '')
        data = tgking.M('module').field('id,status').where(
            'name=?', (module_name,)).select()
        if len(data) == 0:
            tgking.M('module').add('name,status', (module_name, 'start',))
            return tgking.returnJson(True, '开启成功!!')
        else:
            tgking.M('module').where(
                'name=?', (name,)).setField('status', 'start')
            return tgking.returnJson(True, '启动成功!!')

    def disableApi(self):
        module_name = request.form.get('module_name', '')
        data = tgking.M('module').field('id,status').where(
            'name=?', (module_name,)).select()
        if len(data) == 0:
            return tgking.returnJson(True, '停用成功!')
        else:
            tgking.M('module').where('name=?', (module_name,)).delete()
            return tgking.returnJson(True, '停用成功!!')

    def getLastBodyApi(self):
        path = request.form.get('path', '')
        line = request.form.get('line', '100')

        if not os.path.exists(path):
            return tgking.returnJson(False, '文件不存在', (path,))

        try:
            data = tgking.getLastLine(path, int(line))
            return tgking.returnJson(True, 'OK', data)
        except Exception as ex:
            return tgking.returnJson(False, '无法正确读取文件!' + str(ex))

    def runApi(self):
        name = request.form.get('name', '')
        func = request.form.get('func', '')
        args = request.form.get('args', '')
        script = request.form.get('script', 'index')

        data = self.run(name, func, args, script)
        if data[1] == '':
            r = tgking.returnJson(True, "OK", data[0].strip())
        else:
            r = tgking.returnJson(False, data[1].strip())
        return r

    # shell 调用
    def run(self, name, func, args='', script='index'):
        path = self.__module_dir + '/' + name + '/' + script + '.py'
        if not os.path.exists(path):
            path = self.__module_dir + '/' + name + '/' + name + '.py'

        py = 'python3 ' + path
        if args == '':
            py_cmd = py + ' ' + func
        else:
            py_cmd = py + ' ' + func + ' ' + args

        if not os.path.exists(path):
            return ('', '')
        data = tgking.execShell(py_cmd)

        if tgking.isDebugMode():
            print('run', py_cmd)
            print(data)

        return (data[0].strip(), data[1].strip())
