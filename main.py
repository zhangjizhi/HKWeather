# _*_ coding: utf-8 _*_
import pytest
import time
import os

from config.pytest_config import Const
from framework.common_cmd.cmd_util import SyncCmdTask, AsyCmdTask
from framework.util.PyTestUtil import kill_adb, reportStartScript

scriptFile = r'hk/function_pycase/test_weather.py'

date = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
resultPath = os.path.join(Const.RESULT_PATH, date)
report_path = os.path.join(resultPath, 'report')
log_path = os.path.join(resultPath, "log")
if not os.path.exists(log_path):
    os.makedirs(log_path, exist_ok=True)
debug_log = os.path.join(log_path, "android_log.txt")
error_log = os.path.join(log_path, "android_error.txt")

paramlist = list()
paramlist.append("testscript/" + scriptFile)
paramlist.append("-sq")
paramlist.append("-v")
# paramlist.append("--count=10")
paramlist.append("--alluredir=" + resultPath)

ALLURE = "allure"
genargs = f'{ALLURE} generate {resultPath}  --clean -o {report_path}'
showargs = f'{ALLURE} open  {report_path} -p 34567'

if __name__ == '__main__':
    # SyncCmdTask('adb root').runCmd()
    #抓取日志
    ERRLOG = "start /b adb logcat *:E >> " + error_log
    DEBUGLOG = "start /b adb logcat >> " + debug_log
    android_log_task = AsyCmdTask(ERRLOG).startTask()
    android_error_task = AsyCmdTask(DEBUGLOG).startTask()
    time.sleep(2)
    pytest.main(paramlist)
    android_log_task.stopTask()
    android_error_task.stopTask()
    SyncCmdTask(genargs).runCmdProcess()
    reportStartScript(report_path)
    SyncCmdTask(showargs).runCmdProcess()
