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


def writeLog(log_str):
    tgking.writeModLog('[gpmgr][' + str(bot_id) +
                       '][cmd]:' + log_str, 'gpmgr')
    return True


bot_id = sys.argv[1]
bot_data = tgking.getBotById(bot_id)

if bot_data == {}:
    while True:
        writeLog("no start!")
        time.sleep(3)

bot = telebot.TeleBot(bot_data['token'])


def initBotCmd(bot):
    '''
    初始化命令提出
    '''
    bot.delete_my_commands(scope=None, language_code=None)
    bot.set_my_commands(
        commands=[
            telebot.types.BotCommand("me", "个人信息"),
            telebot.types.BotCommand("ban", "禁言用户"),
            telebot.types.BotCommand("unban", "解除用户封禁"),
            telebot.types.BotCommand("show", "查看Ta的信息")
        ],
    )


@bot.message_handler(commands=['id'])
def hanle_get_chat_id(message):
    if message.chat.type != 'private':
        return True
    bot.reply_to(message, message.chat.id)


@bot.message_handler(commands=['me'])
def hanle_me(message):
    if message.chat.type != 'private':
        return True
    bot.reply_to(message, str(message.from_user.id))


@bot.message_handler(commands=['ban'])
def hanle_ban(message):
    '''
    禁言用户
    '''
    # 在群组才能正常使用
    if message.chat.type != 'supergroup':
        return True

    try:
        if hasattr(message, 'reply_to_message'):
            data = bot.get_chat_member(message.chat.id, message.from_user.id)
            if data['status'] in ('administrator', 'creator'):
                bot.ban_chat_member(
                    message.chat.id, message.reply_to_message.json.from.id)
        else:
            bot.answer_callback_query(message.id, text='你无权操作!')
    except Exception as e:
        writeLog(str(e))


@bot.callback_query_handler(func=lambda call: True)
def callback_query_handler(call):
    if call.data != 'ok':
        bot.answer_callback_query(call.id, text='错误选择!')
        return False

    try:
        bot.promote_chat_member(call.message.chat.id, call.from_user.id)

        bot.delete_message(
            chat_id=call.message.chat.id, message_id=call.message.message_id)
    except Exception as e:
        writeLog(str(e))

    try:
        bot.answer_callback_query(call.id, text='你可以发言了!')
    except Exception as e:
        writeLog(str(e))

    writeLog(str(call))


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

    msg_question, msg_rand_list, msg_right_result = model.randQuestion()
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
    keyboard = []
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
        initBotCmd(bot)
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
