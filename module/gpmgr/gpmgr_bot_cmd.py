# coding:utf-8
# python3 module/admgr/admgr_bot_cmd.py

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


bot_id = sys.argv[1]
bot_data = tgking.getBotById(bot_id)

if bot_data == {}:
    while True:
        print("no start!")
        time.sleep(3)

bot = telebot.TeleBot(bot_data['token'])


def writeLog(log_str):
    if __name__ == "__main__":
        print(log_str)

    now = tgking.getDateFromNow()
    log_file = tgking.getServerDir() + '/logs/module_gpmgr.log'
    tgking.writeLog(now + ':' + log_str, log_file, limit_size=5 * 1024)
    return True


@bot.message_handler(commands=['admgr_chat_id'])
def hanle_get_chat_id(message):
    print(message)
    bot.reply_to(message, message.chat.id)


def runBot(bot):
    try:
        bot.polling()
    except Exception as e:
        writeLog('-----bot error start -------')
        writeLog(str(e))
        writeLog('-----bot error end -------')
        time.sleep(1)
        runBot(bot)

if __name__ == "__main__":

    writeLog('启动成功')
    runBot(bot)
