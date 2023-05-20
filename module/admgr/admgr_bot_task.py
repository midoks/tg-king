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

bot_list = tgking.getBotRangeList('admgr')

print(bot_list)

exit(0)

bot = telebot.TeleBot(cfg['bot']['app_token'])


def writeLog(log_str):
    if __name__ == "__main__":
        print(log_str)

    now = tgking.getDateFromNow()
    log_file = getServerDir() + '/admgr.log'
    tgking.writeLog(now + ':' + log_str, log_file, limit_size=5 * 1024)
    return True


def runBotPushTask():
    plist = getStartExtCfgByTag('push')
    for p in plist:
        try:
            script = p['name'].split('.')[0]
            __import__(script).run(bot)
        except Exception as e:
            writeLog('-----runBotPushTask error start -------')
            writeLog(tgking.getTracebackInfo())
            writeLog('-----runBotPushTask error end -------')


def botPush():
    while True:
        runBotPushTask()
        time.sleep(1)

if __name__ == "__main__":
    # 机器人推送任务
    botPushTask = threading.Thread(target=botPush)
    botPushTask.start()
