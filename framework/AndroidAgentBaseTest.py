# -*- coding: utf-8 -*-
# @Time    : 2022/3/13 15:44
# @Author  : zjz
import time
import os

import allure

from config.pytest_config import Const
from framework.public_functions.device_driver import takeScreen
from framework.pulbic_helper import FindActionFunction
from framework.util import variable_util
from framework.util.logger import Logger
from framework.util.variable_util import PublicVariableHandler


def intial_test_log_path(class_name):
    date = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
    android_log_path = os.path.join(Const.RESULT_PATH, class_name, date)
    if not os.path.exists(android_log_path):
        os.makedirs(android_log_path)
    return android_log_path


detail_pass = '''<b style='color:green;'>描述：</b>{}<br/>
                   <b style='color:green;'>执行参数：</b>{}<br/>
                   <b style='color:green;'>预期值：</b>{}<br/>
                   <b style='color:green;'>实际执行结果：</b>{}<br/>
                   <b style='color:green;'>测试结果：</b>{}<br/>'''

detail_fail = '''<b style='color:red;'>描述：</b>{}<br/>
                   <b style='color:red;'>执行参数：</b>{}<br/>
                   <b style='color:red;'>预期值：</b>{}<br/>
                   <b style='color:red;'>实际执行结果：</b>{}<br/>
                   <b style='color:red;'>测试结果：</b>{}<br/>'''


class AndroidAgentBaseTest():
    app_package = ''
    android_log_path = ''

    def __init__(self, app_package, class_name, case_number, case_name):
        self.app_package = app_package
        self.class_name = class_name
        variable_util.Clear()  # 清理掉公用的变量缓存
        self.android_log_path = intial_test_log_path(class_name)
        self.last_test_pass = True
        self.test_step_detail = ''
        case_name_log_file = os.path.join(self.android_log_path, case_name + '.log')
        Logger.addFileHandler(case_name_log_file)
        allure.dynamic.title(case_number + ' - ' + case_name)

    def parse_and_do_step(self, fun_name, if_last_pass=False, desc=None, params=None, expect_value=None):
        if if_last_pass and not variable_util.GetValueByVariable('last_action_pass'):
            raise Exception(variable_util.GetValueByVariable('last_result'))
        fun = FindActionFunction(fun_name)
        if params is not None:
            params = PublicVariableHandler(params)
            action_result = fun(**params)
        else:
            action_result = fun()
        if action_result is not None and isinstance(action_result, dict):
            this_pass = action_result.get('result') if action_result.get('result') is not None else True
            case_test_result = action_result.get('errMsg') if action_result.get('errMsg') is not None else '通过'
        else:
            case_test_result = '通过'
            this_pass = True
        description_detail = detail_pass if this_pass else detail_fail
        test_result = str(action_result) if action_result is not None else '通过'
        case_test_result = '测试通过' if case_test_result == '' else case_test_result
        self.last_test_pass = self.last_test_pass and this_pass
        expect_value = '无' if expect_value is None else str(expect_value)
        desc = fun_name if desc is None else str(desc)
        description_detail = description_detail.format(
            str(desc),
            str(params).strip('{').strip("}").replace("'", ""),
            expect_value.strip('{').strip("}").replace("'", ""),
            str(test_result).replace("'", ""),
            case_test_result
        )
        self.test_step_detail += description_detail
        if not this_pass:
            takeScreen()
        variable_util.AddVariable('last_action_pass', this_pass)
        variable_util.AddVariable('last_result', action_result)
        return action_result

    def getTestResult(self):
        variable_util.AddVariable('last_case', self.last_test_pass)
        allure.dynamic.description(self.test_step_detail)
        return self.last_test_pass, self.test_step_detail
