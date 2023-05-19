# coding:utf-8

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


if __name__ == "__main__":

    # 机器人推送任务
    botPushTask = threading.Thread(target=botPush)
    botPushTask.start()

    # 机器人其他推送任务
    botPushOtherTask = threading.Thread(target=botPushOther)
    botPushOtherTask.start()

    writeLog('启动成功')
    runBot(bot)
