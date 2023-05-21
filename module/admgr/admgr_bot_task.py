# coding:utf-8

# python3 module/admgr/admgr_bot_task.py

import sys
import io
import os
import time
import re
import json
import base64
import threading


sys.path.append(os.getcwd() + "/class/core")
import tgking

import telebot
from telebot import types
from telebot.util import quick_markup


def writeLog(log_str):
    if __name__ == "__main__":
        print(log_str)

    now = tgking.getDateFromNow()
    log_file = tgking.getServerDir() + '/logs/module_admgr.log'
    tgking.writeLog(now + ':' + log_str, log_file, limit_size=5 * 1024)
    return True


def pushContent(bot, tag='admgr', trigger_time=300):
    # 信号只在一个周期内执行一次|start
    lock_file = tgking.getServerDir() + '/tmp/admgr_lock.json'
    if not os.path.exists(lock_file):
        tgking.writeFile(lock_file, '{}')

    lock_data = json.loads(tgking.readFile(lock_file))
    if tag in lock_data:
        diff_time = time.time() - lock_data[tag]['do_time']
        if diff_time >= trigger_time:
            lock_data[tag]['do_time'] = time.time()
        else:
            return False, 0, 0
    else:
        lock_data[tag] = {'do_time': time.time()}
    tgking.writeFile(lock_file, json.dumps(lock_data))

    # 信号只在一个周期内执行一次|end
    keyboard = [
        [
            types.InlineKeyboardButton(
                text="🅾️代实名lDCApp🙎‍♂️+86接码全天在线🅾️", url='https://t.me/ljh09852')
        ],
        [
            types.InlineKeyboardButton(
                text="香港高防CDN、免实名、试用30天", url='https://www.100dun.com')
        ],
        [
            types.InlineKeyboardButton(
                text="CK资源采集", url='https://ckzy1.com/')
        ],
        [
            types.InlineKeyboardButton(
                text="代付支付宝微信❤️淘宝帮付", url='https://t.me/Uxuanzhenpin')
        ],
        [
            types.InlineKeyboardButton(
                text="💰流量变现💰集团收量", url='https://t.me/taohaozhan')
        ],
        [
            types.InlineKeyboardButton(
                text="🙎‍♂️代实名🙍‍♀️过人脸🅾️国际阿里云腾讯云", url='https://t.me/gjgzs2022')
        ],
        [
            types.InlineKeyboardButton(
                text="倩倩CDN服务器", url='https://t.me/KLT_12'),
            types.InlineKeyboardButton(
                text="💎DigitalVirt(赞助商)", url='https://digitalvirt.com/aff.php?aff=154')
        ],
        [
            types.InlineKeyboardButton(
                text="论坛", url='https://bbs.midoks.me'),
            types.InlineKeyboardButton(
                text="搜索", url='https://bbs.midoks.me/search.php'),
            types.InlineKeyboardButton(
                text="@ME", url='tg://user?id=5568699210'),
            types.InlineKeyboardButton(
                text="100RMB/M", url='tg://user?id=5568699210')
        ]
    ]
    markup = types.InlineKeyboardMarkup(keyboard)

    msg_notice = "由于在解决的问题的时候，不给信息，无法了解情况。以后不再群里回答技术问题。全部去论坛提问。在解决问题的过程中，可能需要面板信息，和SSH信息，如无法提供请不要提问。为了让群里都知晓。轮播一年！\n"
    msg_notice += "为了不打扰双方，私聊解决问题先转100U，否则无视!\n"
    msg = bot.send_message(chat_id, msg_notice, reply_markup=markup)

    # print(msg.message_id)
    time.sleep(60)
    try:
        bot.delete_message(
            chat_id=chat_id, message_id=msg.message_id)
    except Exception as e:
        print(str(e))


def runBotPushTask():
    bot_list = tgking.getBotRangeList('admgr')
    for x in range(len(bot_list)):
        # print(bot_list[x])
        bot = telebot.TeleBot(bot_list[x])
        pushContent(bot)
        time.sleep(1)


def botPush():
    while True:
        runBotPushTask()
        time.sleep(3)

if __name__ == "__main__":
    # 机器人推送任务
    botPushTask = threading.Thread(target=botPush)
    botPushTask.start()
