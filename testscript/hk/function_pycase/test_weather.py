# -*- coding: utf-8 -*-
# @Time    : 2022/3/13 15:44
# @Author  : zjz

import os
import sys

import allure
import pytest

from config.pytest_config import Const
from framework.AndroidAgentBaseTest import AndroidAgentBaseTest
from framework.bussiness_functions.myobservatory_action import startMyObservatoryInit
from framework.public_functions.device_driver import InitViews
from framework.pulbic_helper import formatAfterToday
from framework.util.logger import printf, printe

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), "framework"))
InitViews(Const.PYTEST_SCRIPT_YML + '/function_case/weather/ui.yml')


@allure.feature('HK9-day Weather')
class TestHKWeather():
    app_package = 'hko.MyObservatory_v1_0'
    Const.OPENPERMISSION_ENABLE = True
    test_01_data = [
        {'fun_name': 'click', 'if_last_pass': False, 'desc': 'click left menu', 'params': {'view': '左侧菜单按钮'},
         'expect_value': None},
        {'fun_name': 'checkListContent', 'if_last_pass': True,
         'desc': 'check list text contain 9-Day Forecast',
         'params': {'view': '左侧菜单列表名称', 'text': '9-Day Forecast', 'listView': '左侧菜单列表'},
         'expect_value': None},
        {'fun_name': 'click', 'if_last_pass': True, 'desc': 'click 9-Day Forecast',
         'params': {'view': '9-Day Forecast'}, 'expect_value': None},
        {'fun_name': 'getListTextsByViewValue', 'if_last_pass': True, 'desc': 'check tomorrow forceast',
         'params': {'view': '天气预报列表日期', 'value': formatAfterToday(1),
                    'brothers': ['天气预报列表温度', '天气预报列表湿度', '天气预报列表风', '天气预报列表带伞概率', '天气预报列表天气详情'],
                    'listview': '天气预报列表'}, 'expect_value': None}]
    test_02_data = [{'fun_name': 'sendGet', 'if_last_pass': False, 'desc': 'get 9-day forecast response from Hong Kong Observatory API',
                    'params': {'url': 'https://www.hko.gov.hk/dps/sc/json/DYN_DAT_MINDS_FND.json'},
                    'expect_value': None},
                    {'fun_name': 'getForecastInfoFromResponse', 'if_last_pass': True,
                     'desc': 'get forecast info from response',
                     'params': {'afterdays':2,'response':'${last_result}','list_keys':['MaxRH','MinRH','WindInfo'],'unit':{'RH':'%'}},
                     'expect_value': None},
                    ]

    def testA_hkweather_V1_0_function_01(self):
        startMyObservatoryInit(Const.OPENPERMISSION_ENABLE)
        test = AndroidAgentBaseTest(TestHKWeather.app_package, 'TestHKWeather', 'A_hkweather_V1_0_function_01',
                                    'check tomorrow weather forecast from 9-day forecast screen')
        try:
            for test_param in TestHKWeather.test_01_data:
                result = test.parse_and_do_step(**test_param)
            printf(result)
        except Exception as e:
            printe(str(e))
        last_test_pass, test_step_detail = test.getTestResult()
        assert last_test_pass, str(test_step_detail)

    def testA_hkweather_V1_0_function_02(self):
        test = AndroidAgentBaseTest(TestHKWeather.app_package, 'TestHKWeather', 'A_hkweather_V1_0_function_02',
                                    'today after tomorrow weather forecast info from forecast api')
        try:
            for test_param in TestHKWeather.test_02_data:
                result = test.parse_and_do_step(**test_param)
            printf(result)
        except Exception as e:
            printe(str(e))
        last_test_pass, test_step_detail = test.getTestResult()
        assert last_test_pass, str(test_step_detail)
