# _*_ coding: utf-8 _*_

import subprocess
import os
import traceback
import envoy
import psutil

from framework.util.logger import printf, printe

adb_keep_pid = []


def AddAdbPidNotKill(p):
    adb_keep_pid.append(p.pid)


def runCmd(cmd, timeout=60):
    # printf('Cmd ->:' + cmd.strip(), False)
    # with subprocess.Popen(cmd,
    #                       stdout=subprocess.PIPE,
    #                       stderr=subprocess.PIPE,
    #                       shell=True) as p1:
    #     stdout = p1.stdout.read()
    #     stderr = p1.stderr.read()
    #     data = (stdout + stderr).decode('gbk', 'ignore')
    #     for line in data.splitlines():
    #         printf('Cmd <-:' + line.strip())
    # return data
    printf('Cmd ->:' + cmd.strip(), False)
    r = envoy.run([cmd], timeout=timeout, kill_timeout=timeout)
    stdout = r.std_out
    stderr = r.std_err
    data = stdout + stderr
    for line in data.splitlines():
        printf('Cmd <-:' + line.strip(), False)
    return data


def kill_process(p):
    try:
        printf('kill-process->' + str(p.pid))
        os.kill(p.pid, 9)
    except Exception as e:
        printe(e)


def executeCmd(cmd, code="utf8"):
    print(cmd)
    process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    line = ""
    errline = ""
    while process.poll() is None:
        line = process.stdout.readline()
        line = line.strip()
        if line:
            print(line.decode(code, 'ignore'))
            if len(line) > 20:
                if line.find(("waiting for any device").encode()) >= 0:
                    print("测试设备未连接，无法升级")
                    exit(1)
        if process.stderr:
            errline = process.stderr.readline().strip()
            if errline:
                print(errline.decode(code, 'ignore'))
    return line, errline


def find_all_adb_pid():
    adb_pid_list = list()
    pl = psutil.pids()
    for pid in pl:
        if psutil.Process(pid).name() == 'adb.exe':
            adb_pid_list.append(pid)
    return adb_pid_list


def save_adb_pid_not_kill():
    adb_keep_pid.extend(find_all_adb_pid())
    pass


def kill_adb():
    try:
        print('taskkill -f /im adb.exe')
        return runCmd('taskkill -f /im adb.exe')
    except Exception as e:
        traceback.print_exc()


def GetDevices():
    cmd = "adb devices"
    data, errdata = runCmd(cmd)
    print(data)
    # 被测设备串号列表
    serials = []
    if len(data) <= 2:
        print("No Available Devices found")
        return -1
    else:
        for item in data:
            if 'List' in item:
                continue
            elif 'no permissions' in item:
                print("No permissions of the device")
                print(item)
                continue
            elif len(item.strip()) == 0:
                continue
            else:
                serials.append(item.split()[0])
        return serials


def InitEnv():
    devices = GetDevices()
    if devices == -1:
        return -1
    else:
        cmd = "python -m uiautomator2 init"
        data, errdata = runCmd(cmd)
        print(data)
        if len(data) < 1:
            return -1
        else:
            for item in data:
                if "Successfully init" in item:
                    return 0
    return -1


def reportStartScript(path):
    batFile = os.path.join(path,'start.bat')
    with open(batFile,'w+') as f:
        f.write(f'''@echo off
allure open  ./ -p 34567
pause''')

if __name__ == '__main__':
    reportStartScript('D:/workplace/python/SmartTestF/result/20211203/20211203_094629/report')
