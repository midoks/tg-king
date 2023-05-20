# coding:utf-8

# ---------------------------------------------------------------------------------
# TG全能王面板
# ---------------------------------------------------------------------------------
# copyright (c) 2023-∞(https://github.com/midoks/tg-king) All rights reserved.
# ---------------------------------------------------------------------------------
# Author: midoks <midoks@163.com>
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
# 配置操作
# ---------------------------------------------------------------------------------

import psutil
import time
import os
import sys
import re
import json
import pwd

from flask import session
from flask import request


class config:
    __version = '0.0.1.2'

    def __init__(self):
        pass

    def getVersion(self):
        return self.__version

    def get(self):
        data = {}
        data['status_code'] = 0
        return data
