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


class logs_api:

    def listApi(self):
        limit = request.form.get('limit', '10')
        p = request.form.get('p', '1')

        start = (int(p) - 1) * (int(limit))

        siteM = tgking.M('logs').field('id,type,log,addtime')

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
        r = tgking.M('logs').where("id=?", (tid,)).delete()
        if r < 0:
            return tgking.returnJson(False, '删除失败!')
        return tgking.returnJson(True, '删除成功!')

    def clearApi(self):
        tgking.M('logs').where('id>?', (0,)).delete()
        tgking.writeDbLog('日志管理', '清空成功')
        return tgking.returnJson(True, '清空成功!')
