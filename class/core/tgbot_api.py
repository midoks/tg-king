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

import tgking

from flask import request


class tgbot_api:

    ##### ----- start ----- ###
    def listApi(self):
        limit = request.form.get('limit', '10')
        p = request.form.get('p', '1')

        start = (int(p) - 1) * (int(limit))

        siteM = tgking.M('tg_bot').field('id,alias,token')

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
        r = tgking.M('tg_bot').where("id=?", (tid,)).delete()
        if r < 0:
            return tgking.returnJson(False, '删除失败!')
        return tgking.returnJson(True, '删除成功!')

    def addApi(self):
        token = request.form.get('token', '')
        alias = request.form.get('alias', '')
        tid = request.form.get('id', '')

        if tid != '':
            tgking.M('tg_bot').where('id=?', (tid,)).setField('token', token)
            tgking.M('tg_bot').where('id=?', (tid,)).setField('alias', alias)
            return tgking.returnJson(True, '修改成功!')

        if token == '':
            return tgking.returnJson(False, 'Token不能为空!')

        if not tgking.isAppleSystem():
            cmd = 'source bin/activate &&  python3 tools.py verify_tgbot ' + token
            data = tgking.execShell(cmd)
            return_status = data[0].strip()
            if return_status.find('ok') > -1:
                rlist = return_status.split('|')
                tgking.M('tg_bot').add(
                    'alias,token', (rlist[1], token,))
                return tgking.returnJson(True, '添加成功!')
            return tgking.returnJson(False, "验证失败!\n" + str(data[0]))

        tgking.M('tg_bot').add('alias,token', (alias, token,))

        return tgking.returnJson(True, '添加成功!')
