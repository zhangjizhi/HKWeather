# -*- coding: utf-8 -*-
# @Time    : 2021/11/24 9:33
# @Author  : zjz
import json

import allure

from framework.pulbic_helper import DoStepAction
from framework.util.http_request import RequestGet, RequestPost

baseurl = "http://127.0.0.1:9005/"
header = {"Accept-Language": "zh-CN,zh;", "Connection": "close", "Content-Type": "application/json; charset=UTF-8"}


@allure.step('执行 http get 请求')
@DoStepAction(action_description='get 请求')
def sendGet(url):
    if 'http' not in url:
        url = baseurl + url
    result, is_pass = RequestGet(url)
    if is_pass:
        code = result.status_code
        if code == 200:
            result = json.loads(result.text)
            return result
        else:
            raise Exception(code)
    else:
        raise Exception(result)


@allure.step('执行 post 请求')
@DoStepAction(action_description='post 请求')
def sendPost(url, data=None):
    if 'http' not in url:
        url = baseurl + url
    result, is_pass = RequestPost(url=url, data=data)
    if is_pass:
        code = result.status_code
        if code == 200:
            result = json.loads(result.text)
            return result
        else:
            raise Exception(code)
    else:
        raise Exception(result)
