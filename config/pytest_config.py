# -*- coding: utf-8 -*-
# @Time    : 2021/11/25 14:53
# @Author  : zjz
import datetime
import os




class Const:
    # 路径
    PYTEST_ROOT = os.path.dirname(os.path.dirname(__file__))
    today = datetime.datetime.now().strftime("%Y%m%d")
    # result 路径
    RESULT_PATH = os.path.join(PYTEST_ROOT, 'result', today)
    # screenshot 路径
    SCREENSHOT_PATH = os.path.join(RESULT_PATH, 'screenshot')

    RESOURCE_PATH = os.path.join(PYTEST_ROOT, 'resource', 'pic')

    PYTEST_SCRIPT_ROOT = os.path.join(PYTEST_ROOT, 'testscript', 'hk')

    PYTEST_SCRIPT_YML = os.path.join(PYTEST_SCRIPT_ROOT, 'PageMapping')
    TOAST_LEFT, TOAST_TOP, TOAST_RIGHT, TOAST_BOTTOM = [920, 840, 1000, 860]
    RESOURCE_COLOR_FILE = os.path.join(PYTEST_ROOT,'resource','pic','color.yml')
    RESOURCE_PIC_PATH = os.path.join(PYTEST_ROOT,'resource','pic')
    OPENPERMISSION_ENABLE = False


