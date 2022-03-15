# -*- coding: utf-8 -*-
# @Time    : 2022/3/13 15:44
# @Author  : zjz
import datetime
import importlib
import os
import traceback
from collections import Counter

from config.view_config import index_en_zh_map
from framework.util.logger import printe
from framework.util.public_function import GetRandom


class DoStepAction:
    def __init__(self, action_description):
        self.action_description = action_description

    def __call__(self, fun):
        def wrapper(*key, **kwargs):
            try:
                do_result = fun(*key, **kwargs)
                if do_result is not None:
                    return do_result
                elif fun.__name__ == 'getWidget':
                    return do_result
                else:
                    return {'result': True, 'errMsg': ''}
            except Exception as e:
                traceback.print_exc()
                printe(traceback.format_exc())
                return {'result': False, 'errMsg': f'{self.action_description}失败：" + {e}'}

        return wrapper


def findDupList(data: list):
    d = dict(Counter(data))
    result = dict((key, value) for key, value in d.items() if value > 1)
    return result


def findListByIndex(widget, index):
    if index not in ['all', 'last', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
        index = index_en_zh_map.get(index)
    if index is not None:
        if str(index).isnumeric():
            index = int(index)
            if index >= len(widget):
                index = len(widget) - 1
            widget = widget[index]
        elif index == 'last':
            index = widget.count - 1
            widget = widget[index]
        elif index == '随机':
            widget = GetRandom(widget)
    return widget


def FindFunction(module_dir, module_package, function_name):
    def function_inner(path):
        file_list = os.listdir(path)
        for file_name in file_list:
            file_abs = os.path.join(path, file_name)
            if os.path.isdir(file_abs):
                function_inner(file_abs)
            else:
                if str(file_name).endswith('.py') and file_name != '__init__.py':
                    file_name = file_name.replace('.py', '')
                    function_model = importlib.import_module(module_package + '.' + file_name)
                    funs = dir(function_model)
                    for item in funs:
                        if item == function_name:
                            fun = getattr(function_model, item)
                            type_str = str(type(fun))
                            if type_str == '<class \'function\'>':
                                return fun

    return function_inner(module_dir)


file_dir = os.path.dirname(__file__)


def FindActionFunction(function_name):
    module_package = 'framework.public_functions'
    module_dir = os.path.join(file_dir, 'public_functions')
    function = FindFunction(module_dir, module_package, function_name)
    if not function:
        module_package = 'framework.bussiness_functions'
        module_dir = os.path.join(file_dir, 'bussiness_functions')
        function = FindFunction(module_dir, module_package, function_name)
    return function


def FindAllAssertFunction(assert_name):
    module_package = 'framework.assert_functions'
    module_dir = os.path.join(file_dir, 'assert_functions')
    function = FindFunction(module_dir, module_package, assert_name)
    return function


def formatAfterToday(days, format='%d %b'):
    today = datetime.date.today()
    next_day = today + datetime.timedelta(days=days)
    return next_day.strftime(format)


def findDicData(key, data):
    try:
        if isinstance(data, dict):
            if key in data:
                return data[key]
            else:
                for item, value in data.items():
                    result = findDicData(key, value)
                    if result is not None:
                        return result
        else:
            return None
    except:
        return None
