# coding: utf-8

import re
import os
import sys
import orm

sys.path.append(os.getcwd() + "/class/core")
import tgking


def unameMosaic(uname):
    '''
    对用户名打马赛克
    '''
    if len(uname) > 4:
        return '%s██%s' % (uname[0:2], uname[-2:])
    return '%s██%s' % (uname[0:1], uname[-1:])
