# coding:utf-8

# python3 module/clientmgr/clientmgr_client_task.py

import sys
import io
import os
import time
import re
import json
import base64
import threading
import asyncio
import logging

sys.path.append(os.getcwd() + "/class/core")
import tgking

import telebot
from telebot import types
from telebot.util import quick_markup

from telethon import TelegramClient


def writeLog(log_str):
    if __name__ == "__main__":
        print(log_str)

    now = tgking.getDateFromNow()
    log_file = tgking.getServerDir() + '/logs/module_clientmgr.log'
    tgking.writeLog(now + ':' + log_str, log_file, limit_size=5 * 1024)
    return True


client_id = sys.argv[1]
client_data = tgking.getClientById(client_id)


tg_id = 'tgking_' + client_id
tg_id_file = tg_id + '.session'

# tg_id_file_ok = tg_id + '_source.session'
# print(tg_id_file_ok)

# c = tgking.readBinFile(tg_id_file_ok)
# c = base64.b64encode(c)
# tgking.M('tg_client').where(
#     'id=?', (client_id,)).setField('data', c)

if not os.path.exists(tg_id_file):
    dedata = base64.b64decode(client_data['data'])
    tgking.writeBinFile(tg_id_file, dedata)

if client_data == {}:
    while True:
        writeLog("clientmgr no start!")
        time.sleep(3)


# print(client_data)
client = TelegramClient(tg_id, client_data['app_id'], client_data['app_hash'])


async def client_run_task():
    writeLog("aaa")
    await client.send_message('me', 'TG全能王验证通过!!')
    time.sleep(10)

async def client_run():
    while True:
        await client_run_task()
        time.sleep(1)

async def main(loop):
    await client.start()

    # create new task
    writeLog('creating telegram client task.')
    task = loop.create_task(client_run())
    await task

    writeLog('It works.')
    await client.run_until_disconnected()
    task.cancel()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
