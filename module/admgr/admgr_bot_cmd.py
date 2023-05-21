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

    writeLog('启动成功')
    runBot(bot)
