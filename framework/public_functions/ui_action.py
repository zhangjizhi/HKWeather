# -*- coding: utf-8 -*-
# @Time    : 2022/3/13 15:44
# @Author  : zjz

import allure
import time
import random
import cv2
import os

# 点击控件
from framework.public_functions.device_driver import getChildren, getWidget
from framework.pulbic_helper import DoStepAction


@allure.step('执行点击控件')
@DoStepAction(action_description='点击控件')
def click(view, parentView=None, parentIndex=0, index=0, times=1, sleep=1):
    if parentView and view:
        widget = getChildren(parentView, view, parentIndex, index)
    else:
        widget = getWidget(view, index)
    if widget is not None:
        for i in range(times):
            if isinstance(widget, list):
                widget = widget[0]
            widget.click()
            time.sleep(sleep)
    else:
        raise Exception(f"父元素{parentView}父位置{parentIndex}元素{view}位置{index}不存在")
