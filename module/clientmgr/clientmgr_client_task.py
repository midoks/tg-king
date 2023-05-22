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

if client_data == {}:
    while True:
        writeLog("clientmgr no start!")
        time.sleep(3)


print(client_data)
client = TelegramClient('tgking_' + client_id, client_data[
                        'app_id'], client_data['app_hash'])


async def client_run_task():
    print('aaa')

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
