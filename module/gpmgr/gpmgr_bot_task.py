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
    tgking.writeModLog('[gpmgr][task]:' + log_str, 'gpmgr')
    return True


chat_id = 5568699210


def pushContent(bot, tag='gpmgr', trigger_time=300):
    # 信号只在一个周期内执行一次|start
    lock_file = tgking.getServerDir() + '/tmp/gpmgr_lock.json'
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

    msg_notice = "全能王测试\n"
    msg = bot.send_message(chat_id, msg_notice, reply_markup=markup)

    time.sleep(60)
    try:
        bot.delete_message(
            chat_id=chat_id, message_id=msg.message_id)
    except Exception as e:
        writeLog("admgr:\n" + str(e))


def runBotPushTask():
    bot_list = tgking.getBotRangeList('gpmgr')
    for x in range(len(bot_list)):
        # print(bot_list[x]['token'])
        bot = telebot.TeleBot(bot_list[x]['token'])
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
