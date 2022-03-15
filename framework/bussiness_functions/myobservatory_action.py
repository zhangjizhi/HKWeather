# -*- coding: utf-8 -*-
# @Time    : 2022/3/13 13:17
# @Author  : zjz
import ast
import json
import re
import time

import allure

from framework.public_functions.device_driver import getWidget, appStart, appStop, back
from framework.public_functions.ui_action import click
from framework.pulbic_helper import DoStepAction, formatAfterToday, findDicData


@allure.step('初始化app')
@DoStepAction(action_description='初始化app')
def startMyObservatoryInit(need):
    appStop('hko.MyObservatory_v1_0')
    appStart('hko.MyObservatory_v1_0')
    time.sleep(3)
    if need:
        while getWidget(view='hko.MyObservatory_v1_0:id/btn_agree'):
            click(view='hko.MyObservatory_v1_0:id/btn_agree')
        if getWidget(view='android:id/button1'):
            click(view='android:id/button1')
            click(view='com.android.permissioncontroller:id/permission_allow_always_button')
            time.sleep(3)
            getWidget(view='hko.MyObservatory_v1_0:id/whatsNewContent')
            back()
            time.sleep(3)


@allure.step('从天气预报api获取天气信息')
@DoStepAction(action_description='从天气预报api获取天气信息')
def getForecastInfoFromResponse(afterdays, response, list_keys: list, unit: dict):
    need_day = formatAfterToday(afterdays, '%Y%m%d')
    response_str = json.dumps(response, ensure_ascii=False) if not isinstance(response, str) else response
    p = re.compile(f'["\']Day[1-9]ForecastDate[\"\'].+?[\'"]{need_day}[\'"]')
    result = re.findall(p, response_str)
    if result:
        result_dic = {}
        position = re.findall(re.compile('Day([1-9])ForecastDate'), result[0])[-1]
        list_keys = [f'Day{position}' + x for x in list_keys]
        if isinstance(response, str):
            try:
                response = json.loads(response)
            except:
                response = ast.literal_eval(response)
        for key in list_keys:
            value = findDicData(key, response)['Value_Eng']
            if key.startswith(f'Day{position}Max'):
                key = key.replace(f'Day{position}Max', '').strip()
                value = result_dic.get(key) + value if result_dic.get(key) is not None else '- ' + value
            elif key.startswith(f'Day{position}Min'):
                key = key.replace(f'Day{position}Min', '').strip()
                value = value + '' + result_dic.get(key) if result_dic.get(key) is not None else value + '- '
            result_dic[key] = value
        for key, value in result_dic.items():
            result_dic[key] = value + unit.get(key) if unit.get(key) is not None else value
        return {need_day: result_dic}
    else:
        raise Exception(f'找不到日期{need_day}')
