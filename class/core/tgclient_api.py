# coding:utf-8

# ---------------------------------------------------------------------------------
# TG全能王面板
# ---------------------------------------------------------------------------------
# copyright (c) 2023-∞(https://github.com/midoks/tg-king) All rights reserved.
# ---------------------------------------------------------------------------------
# Author: midoks <midoks@163.com>
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
# 机器人操作API
# ---------------------------------------------------------------------------------

import os
import time

import tgking

from flask import request


class tgclient_api:

    ##### ----- start ----- ###
    def listApi(self):
        limit = request.form.get('limit', '10')
        p = request.form.get('p', '1')

        start = (int(p) - 1) * (int(limit))

        siteM = tgking.M('tg_client').field('id,app_id,app_hash,is_vaild')

        _list = siteM.limit((str(start)) + ',' +
                            limit).order('id desc').select()

        count = siteM.count()

        _ret = {}
        _ret['code'] = 0
        _ret['msg'] = 'ok'
        _ret['data'] = _list
        _ret['count'] = count

        return tgking.getJson(_ret)

    def delApi(self):
        tid = request.form.get('id', '')
        r = tgking.M('tg_client').where("id=?", (tid,)).delete()
        if r < 0:
            return tgking.returnJson(False, '删除失败!')
        return tgking.returnJson(True, '删除成功!')

    def addApi(self):
        app_id = request.form.get('app_id', '')
        app_hash = request.form.get('app_hash', '')
        tid = request.form.get('id', '')

        if app_id == '':
            return tgking.returnJson(False, 'app_id不能为空!')

        if app_hash == '':
            return tgking.returnJson(False, 'app_hash不能为空!')

        if tid != '':
            tgking.M('tg_client').where(
                'id=?', (tid,)).setField('app_id', app_id)
            tgking.M('tg_client').where(
                'id=?', (tid,)).setField('app_hash', app_hash)
            return tgking.returnJson(True, '修改成功!')

        tgking.M('tg_client').add('app_id,app_hash', (app_id, app_hash,))

        return tgking.returnJson(True, '添加成功!')

    def resetVaildApi(self):
        tid = request.form.get('id', '')

        tgking.M('tg_client').where(
            'id=?', (tid,)).setField('is_vaild', 0)

        tgking.M('tg_client').where(
            'id=?', (tid,)).setField('data', '')

        return tgking.returnJson(0, '重置成功!')

    def vaildApi(self):
        tid = request.form.get('id', '')
        tel = request.form.get('tel', '')

        session_tg = 'tgking_' + tid + '.session'
        if os.path.exists(session_tg):
            os.remove(session_tg)

        tmp_path = '/tmp/tg_vaild_tel_' + tid
        tgking.writeFile(tmp_path, tel)

        cmd = 'source bin/activate &&  python3 tools.py verify_tgclient ' + tid + ' &'
        os.system(cmd)

        err_path = '/tmp/tg_vaild_err_' + tid

        for x in range(5):
            if os.path.exists(err_path):
                err = tgking.readFile(err_path)
                os.remove(err_path)
                return tgking.returnCode(-1, err)
            time.sleep(1)
        return tgking.returnCode(0, '验证中,注意查看短码!')

    def vaildCodeApi(self):
        tid = request.form.get('id', '')
        code = request.form.get('code', '')
        pwd = request.form.get('pwd', '')

        ''' debug
        echo "+86xxxx" >/tmp/tg_vaild_tel_3
        echo "77692" > /tmp/tg_vaild_code_3
        echo "xxxx" > /tmp/tg_vaild_pwd_3
        source bin/activate &&  python3 tools.py verify_tgclient 3
        python3 module/clientmgr/clientmgr_client_task.py 3
        '''

        tmp_path = '/tmp/tg_vaild_code_' + tid
        tgking.writeFile(tmp_path, code)

        tmp_path = '/tmp/tg_vaild_pwd_' + tid
        tgking.writeFile(tmp_path, pwd)

        tmp_err_path = '/tmp/tg_vaild_err_' + tid

        for x in range(10):
            ok_path = '/tmp/tg_vaild_ok_' + tid
            if os.path.exists(ok_path):
                tgking.M('tg_client').where(
                    'id=?', (tid,)).setField('is_vaild', 1)

                session_tg = 'tgking_' + tid + '.session'
                # print(session_tg)
                # print(tgking.readBinFile(session_tg))
                tgking.M('tg_client').where(
                    'id=?', (tid,)).setField('data', tgking.readBinFile(session_tg))
                os.remove(ok_path)

                tmp_tel_path = '/tmp/tg_vaild_tel_' + tid
                if os.path.exists(tmp_tel_path):
                    os.remove(tmp_tel_path)

                return tgking.returnCode(0, '验证成功!')
            time.sleep(1)
        err_msg = ''
        if os.path.exists(tmp_err_path):
            err_msg = tgking.readFile(tmp_err_path)
            os.remove(tmp_err_path)
        return tgking.returnCode(-1, "验证失败!\n" + err_msg)
