# -*- coding: utf-8 -*-
# @Time    : 2022/3/12 15:44
# @Author  : zjz
import json
import psutil
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from framework.util.logger import printe

header = {"Accept-Language": "zh-CN,zh;", "Connection": "close", "Content-Type": "application/json; charset=UTF-8"}
proxies = {
    'http': '127.0.0.1:9005',
}


def GetProcessExit(process_name):
    try:
        pl = psutil.pids()
        for pid in pl:
            if psutil.Process(pid).name() == process_name:
                return True
        return False
    except Exception as e:
        printe(e)
        return False


def RequestGet(url):
    try:
        if GetProcessExit('Fiddler.exe'):
            response = _RequestRetrySession().get(url, headers=header, proxies=proxies)
        else:
            response = _RequestRetrySession().get(url, headers=header)

        if response.headers.get("sessionId"):
            header['sessionId'] = response.headers.get("sessionId")
        return response, True
    except Exception as e:
        printe(e)
        printe("get url fail:%s" % url)
        return str(e), False


def RequestPost(url, data):
    try:
        if data:
            dataJson = json.dumps(data, ensure_ascii=False)
            if GetProcessExit('Fiddler.exe'):
                response = _RequestRetrySession().post(url, headers=header, data=dataJson.encode(), timeout=60,
                                                       proxies=proxies)
            else:
                response = _RequestRetrySession().post(url, headers=header, data=dataJson.encode(), timeout=60)

        else:
            response = _RequestRetrySession().post(url, headers=header, data=None, timeout=60)
        return response, True
    except Exception as e:
        printe(str(e))
        raise e
        return str(e), False


def _RequestRetrySession(retries=1,
                         backoff_factor=0.3,
                         status_forcelist=(500, 502, 504),
                         session=None):
    requests.adapters.DEFAULT_RETRIES = 5
    session = session or requests.Session()
    session.keep_alive = False
    retry = Retry(total=retries,
                  read=retries,
                  connect=retries,
                  backoff_factor=backoff_factor,
                  status_forcelist=status_forcelist)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    return session
