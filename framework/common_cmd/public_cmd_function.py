# -*- coding: utf-8 -*-
# @Time    : 2021/11/23 15:31
# @Author  : zjz
import os
import re

from framework.common_cmd.cmd_util import SyncCmdTask
from framework.common_cmd.command import GetDevices, GetAppStartActivity, GetWindowPolicy, GetInstalledApp, \
    GetInstallApk
from framework.util.PyTestUtil import kill_adb


def FindDevices():
    cmd_task = SyncCmdTask(GetDevices())
    out, err = cmd_task.runCmd(timeout=0.5)
    list_str = str(out).splitlines()
    if list_str and len(list_str) > 2:
        patter = re.compile(r'([a-zA-Z0-9]+)\t')
        result = re.findall(patter, list_str[1])
        if result:
            return result[0]


def CheckAppInstall(package):
    out, err = SyncCmdTask(GetInstalledApp(package)).runCmd()
    if out and package in out:
        return True


def InstallApp(path):
    out, err = SyncCmdTask(GetInstallApk(path))
    if not err:
        return True


def FindStartActivityByPackage(package):
    task = SyncCmdTask(GetAppStartActivity(package))
    out, err = task.run_cmd(timeout=3)
    if out:
        patter = re.compile(f'({package}/[a-zA-Z0-9\.]+) filter')
        result = re.findall(patter, out)
        if result:
            return result[0]


def LightScreen():
    stdout, stderr = SyncCmdTask(GetWindowPolicy()).runCmd()
    if stdout:
        if 'mShowingLockscreen=true' in stdout:
            if 'mScreenOnEarly=false' in stdout:
                os.system('adb shell input keyevent 26')
            os.system('adb shell input keyevent 82')


def PytestInit():
    SyncCmdTask('adb root').runCmd()
    SyncCmdTask('python -m uiautomator2 init').runCmd()
    SyncCmdTask('adb logcat -c').runCmd()
    kill_adb()
