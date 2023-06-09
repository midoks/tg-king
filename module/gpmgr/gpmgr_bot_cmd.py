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
    tgking.writeModLog('[gpmgr][' + str(bot_id) +
                       '][cmd]:' + log_str, 'gpmgr')
    return True


@bot.message_handler(commands=['id'])
def hanle_get_chat_id(message):
    if message.chat.type != 'private':
        return True
    bot.reply_to(message, message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_query_handler(call):
    #
    print(call)
    msg = call.text
    writeLog('msg:' + str(msg))


@bot.message_handler(func=lambda message: True)
def all_message(message):
    writeLog('msg:' + str(message))


@bot.message_handler(content_types=["new_chat_members"])
def onNewUser(message):
    writeLog('new_chat_members:' + str(message))
    # bot.send_message(message, "running onNewUser")


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
