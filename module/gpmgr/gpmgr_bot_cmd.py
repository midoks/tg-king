# coding:utf-8

'''
cd /opt/tg-king && source bin/activate && python3 module/gpmgr/gpmgr_bot_cmd.py 1
'''

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

sys.path.append(os.getcwd() + "/module/gpmgr/class")
import model


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
    print(call)

    try:
        bot.promote_chat_member(call.message.chat.id, call.from_user.id)

        bot.delete_message(
            chat_id=call.message.chat.id, message_id=call.message.message_id)
    except Exception as e:
        writeLog(str(e))

    try:
        bot.answer_callback_query(id=call.id, text='你可以发言了!')
    except Exception as e:
        writeLog(str(e))


@bot.message_handler(func=lambda message: True)
def all_message(message):
    writeLog('msg:' + str(message))


@bot.message_handler(content_types=["left_chat_member"])
def handle_left_chat_member(message):
    # 删除入群消息
    try:
        bot.delete_message(
            chat_id=message.chat.id, message_id=message.message_id)
    except Exception as e:
        writeLog(str(e))


@bot.message_handler(content_types=["new_chat_members"])
def handle_new_chat_members(message):
    '''
    新加入的用户
    '''

    try:
        # 删除入群消息
        bot.delete_message(
            chat_id=message.chat.id, message_id=message.message_id)

        # 限制入群权限
        bot.restrict_chat_member(message.chat.id, message.from_user.id)

    except Exception as e:
        writeLog(str(e))

    msg_question, msg_rand_list, msg_right_result = randQuestion()
    question_choose = []

    for rand_result in msg_rand_list:
        t = None
        if rand_result == msg_right_result:
            t = types.InlineKeyboardButton(
                text=str(rand_result), callback_data='ok')
        else:
            t = types.InlineKeyboardButton(
                text=str(rand_result), callback_data=str(rand_result))
        question_choose.append(t)

    # 发送验证消息

    # [
    #     types.InlineKeyboardButton(
    #         text="1", callback_data='1'),
    #     types.InlineKeyboardButton(
    #         text="2", callback_data='2'),
    #     types.InlineKeyboardButton(
    #         text="3", callback_data='3'),
    #     types.InlineKeyboardButton(
    #         text="4", callback_data='4')
    # ]
    keyboard = []
    keyboard.append(question_choose)
    keyboard.append(
        [
            types.InlineKeyboardButton(
                text="允许(管理员)", callback_data='5'),
            types.InlineKeyboardButton(
                text="禁止(管理员)", callback_data='6')
        ]
    )

    markup = types.InlineKeyboardMarkup(keyboard)

    # 1+1=❓
    try:
        question = "[%s](tg://user?id=%s) 本群开启入群验证,请尽快完成验证才可问题后才可进群发言!\n请回答问题:%s" % (
            model.unameMosaic(message.from_user.first_name), message.from_user.id, msg_question)
        bot.send_message(message.chat.id, question,
                         parse_mode='Markdown', reply_markup=markup)
    except Exception as e:
        writeLog(str(e))


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
