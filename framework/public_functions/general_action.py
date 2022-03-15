# -*- coding: utf-8 -*-
# @Time    : 2021/11/24 10:18
# @Author  : zjz
import time

import allure

# 此方法用于两个 variable 储存的比较。
from framework.pulbic_helper import DoStepAction
from framework.util import variable_util


@allure.step('执行此方法用于两个variable储存的比较')
@DoStepAction(action_description='比较公共参数')
def compareVariable(key1, key2):
    text1 = variable_util.GetValueByVariable(key1)
    text2 = variable_util.GetValueByVariable(key2)
    if text1 != text2:
        return {'result': False, 'errMsg': "variable 储存值" + str(text1) + "  和预期值 " + str(text2) + "不相等"}
    else:
        return {'result': True, 'errMsg': ""}


@allure.step('执行设置一个公共变量')
@DoStepAction(action_description='执行设置一个公共变量')
def setVariable(key, value):
    variable_util.AddVariable(key, value)


@allure.step('执行等待x秒')
@DoStepAction(action_description='等待x秒')
def waitSeconds(sleep):
    time.sleep(sleep)
