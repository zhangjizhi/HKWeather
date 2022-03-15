# _*_ coding: utf-8 _*
import json
import os
import re

from framework.util.logger import printf, printe

tread_variable = {}


def Clear():
    tread_variable.clear()


def GetValueByVariable(key):
    printf(tread_variable)
    if key in tread_variable.keys():
        return tread_variable[key]
    else:
        return None


def AddVariable(key, value):
    tread_variable[key] = value


def DelVariable(key):
    del tread_variable[key]


def PublicVariableHandler(expect_value):
    try:
        if expect_value and len(expect_value) > 0:
            expect_str = json.dumps(expect_value, ensure_ascii=False)
            pattner = re.compile(r'\$\{(.+?)\}')
            variable_keys = re.findall(pattner, expect_str)
            variable_keys = list(set(variable_keys))
            if variable_keys and len(variable_keys) > 0:
                for item in variable_keys:
                    item_value = GetValueByVariable(item)
                    if item_value is not None:
                        item_str = "${%s}" % item
                        excepted_str = expect_str.replace(str(item_str), str(item_value))
                        excepted_str = excepted_str.replace('\\', '/')
                    expect_value = json.loads(excepted_str)
    except Exception as e:
        printe(str(e))
    return expect_value
