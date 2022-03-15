#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import threading
from threading import Timer
import traceback

from framework.util.logger import printe, printf


def runCmd(cmd):
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) as p1:
        data = p1.stdout.read().decode('gbk', 'ignore').splitlines()
        for d in data:
            if d and len(d) > 0:
                print(d)
        errdata = p1.stderr.read().decode('gbk', 'ignore').splitlines()
        for err in errdata:
            if err and len(err) > 0:
                print(err)
        return data, errdata


class RunCmdUtil(object):
    '''
    执行测试命令类
    '''

    def __init__(self, cmd, errFileFullPath=None, logFileFullPath=None):
        """
        初始化类
        :param timeout: 每隔多久检查是否退出
        :param cmd: 运行的命令
        :param errFileFullPath:
        :param logFileFullPath:
        :return:
        """
        self.cmd = cmd
        if logFileFullPath:
            self.stdout = open(logFileFullPath, 'w+')
        if errFileFullPath:
            self.stderr = open(errFileFullPath, 'a+')
        self.p = None
        self.my_timer = None

    def stop_cmd_thread(self):
        try:
            if self.p:
                kill_process(self.p)
                self.p = None
            if self.my_timer and self.my_timer.is_alive():
                self.my_timer.cancel()
        except Exception as e:
            printe(traceback.format_exc())

    def timeout_callback(self, p):
        '''
        定时函数回调执行函数
        :param p: 进程
        :return:
        '''

        try:
            kill_process(p)
        except Exception as error:
            printe(traceback.format_exc())

    def _runCmd(self, timeout=None):
        '''
        执行测试等待测试结束
        :return:
        '''
        self.p = subprocess.Popen(self.cmd, stdout=self.stdout.fileno(), stderr=self.stderr.fileno(), shell=True)
        if timeout:
            self.my_timer = Timer(timeout, self.timeout_callback, [self.p])
            self.my_timer.start()
        printf("开始执行%s------pid:%d" % (self.cmd, self.p.pid))
        try:
            self.p.wait()
        except Exception as e:
            printe(traceback.format_exc())
        finally:
            if self.my_timer and self.my_timer.is_alive():
                self.my_timer.cancel()

    def start_cmd_thread(self, timeout=None):
        if self.p:
            self.stop_cmd_thread()
        log_thread = threading.Thread(target=self._runCmd, args=(timeout,))
        log_thread.start()
