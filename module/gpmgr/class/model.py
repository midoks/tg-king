# coding: utf-8

import re
import os
import sys
import random

# sys.path.append(os.getcwd() + "/class/core")
# import tgking


def unameMosaic(uname):
    '''
    对用户名打马赛克
    '''
    if len(uname) > 4:
        return '%s██%s' % (uname[0:2], uname[-2:])
    return '%s██%s' % (uname[0:1], uname[-1:])


def randQuestion():
    '''
    随机生成问题
    '''
    q1 = random.randint(0, 100)
    q2 = random.randint(0, 100)
    asum = q1 + q2

    question = str(q1) + '+' + str(q2) + ' = ❓'

    slist = []
    for x in range(5):
        t = random.randint(0, 199)
        slist.append(t)
    slist.append(asum)
    random.shuffle(slist)
    return question, slist, asum


if __name__ == '__main__':
    msg_question, msg_rand_list, msg_right_result = randQuestion()
    for x in msg_rand_list:
        print(x)
