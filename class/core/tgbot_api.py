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
        type_id = request.form.get('type_id', '0').strip()

        start = (int(p) - 1) * (int(limit))

        siteM = tgking.M('sites').field('id,name,path,status,ps,addtime,edate')
        if type_id != '' and int(type_id) >= 0:
            siteM.where('type_id=?', (type_id,))

        _list = siteM.limit((str(start)) + ',' +
                            limit).order('id desc').select()

        for i in range(len(_list)):
            _list[i]['backup_count'] = mw.M('backup').where(
                "pid=? AND type=?", (_list[i]['id'], 0)).count()

        _ret = {}
        _ret['data'] = _list

        count = siteM.count()
        _page = {}
        _page['count'] = count
        _page['tojs'] = 'getWeb'
        _page['p'] = p
        _page['row'] = limit

        _ret['page'] = tgking.getPage(_page)
        return tgking.getJson(_ret)

    def addApi(self):
        token = request.form.get('token', '')
        if token == '':
            return tgking.returnJson(False, 'Token不能为空!')

        if not tgking.isAppleSystem():
            try:
                import telebot
                bot = telebot.TeleBot(token)
                user = bot.get_me()

                tgking.M('tg_bot').add(
                    'alias,token', (user.first_name, token,))

                return tgking.returnJson(True, '添加成功!')
            except Exception as e:
                return tgking.returnJson(False, '验证失败!')

        tgking.M('tg_bot').add('alias,token', ('默认', token,))

        return tgking.returnJson(True, '添加成功!')
