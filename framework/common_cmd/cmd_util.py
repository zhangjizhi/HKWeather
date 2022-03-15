# coding = utf-8
import os
import subprocess
import threading
import time
import traceback
from collections import deque
import envoy
from framework.util.logger import printe, printf


class CmdBase:
    my_process_list = []

    def __init__(self, cmd):
        self._cmd = cmd
        self._p = None
        self._running = False

    @staticmethod
    def kill_process(p):
        try:
            printf('kill-process->' + str(p.pid))
            os.kill(p.pid, 9)
        except Exception:
            traceback.print_exc()

    @staticmethod
    def kill_all_process():
        for p in CmdBase.my_process_list:
            CmdBase.kill_process(p)

    def stopTask(self):
        try:
            self._running = False
            if self._p:
                self.kill_process(self._p)
                time.sleep(1)
                self._p = None
        except Exception:
            printe(traceback.format_exc())
        finally:
            self._running = False


class AsyCmdTask(CmdBase):
    task_lock = threading.RLock()

    def __init__(self, cmd, key_word='', stdout=False):
        super().__init__(cmd)
        self.stdout = stdout
        if stdout:
            self.key_word = key_word
            self.cmd_data = deque()

    def __execCmd(self):
        try:
            self._running = True
            self._p = subprocess.Popen(self._cmd,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       shell=True)
            self._p.wait()
        except Exception:
            self.kill_process(self._p)
            printe(traceback.format_exc())
        finally:
            self._running = False

    def __readStdout(self):
        time.sleep(1)
        while self._running:
            try:
                char = self._p.stdout.read(1)
                if char:
                    line = self._p.stdout.readline().decode('GBK', 'ignore')
                    if line and self.key_word in line:
                        with self.task_lock:
                            self.cmd_data = line
                else:
                    time.sleep(1)
            except Exception:
                printe(traceback.format_exc())

    def startTask(self):
        if self._running:
            self.stopTask()
        log_thread = threading.Thread(target=self.__execCmd)
        log_thread.setDaemon(True)
        log_thread.start()
        if self.stdout:
            log_read_thread = threading.Thread(target=self.__readStdout)
            log_read_thread.start()
            log_read_thread.setDaemon(True)
        return self

    def cmdOutData(self):
        if self._running and self.stdout:
            self.p.stdout.flush()
            with self.task_lock:
                data = self.cmd_data.pop() if self.cmd_data else None
            return data


class SyncCmdTask(CmdBase):

    def runCmd(self, timeout=10):
        printf('Cmd ->:' + str(self._cmd), False)
        if isinstance(self._cmd, list):
            r = envoy.run(self._cmd, timeout=timeout, kill_timeout=timeout)
        else:
            r = envoy.run([self._cmd], timeout=timeout, kill_timeout=timeout)
        stdout = r.std_out
        stderr = r.std_err
        return stdout, stderr

    def runCmdProcess(self):
        printf('Cmd ->:' + self._cmd, False)
        with subprocess.Popen(self._cmd,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              shell=True) as p1:
            stdout = p1.stdout.read()
            stderr = p1.stderr.read()
            data = (stdout + stderr).decode('gbk', 'ignore')
            for line in data.splitlines():
                printf('Cmd <-:' + line.strip())
        return data

    # def runCmdTask(self):
    #     # printf('Cmd ->:' + self.cmd.strip(), False)
    #     def run_cmd():
    #         with subprocess.Popen(self.cmd,
    #                               stdout=subprocess.PIPE,
    #                               stderr=subprocess.PIPE,
    #                               shell=True) as p1:
    #             CmdBase.my_process_list.append(p1)
    #             stderr = p1.stderr.read()
    #             p1.wait()
    #             # stdout = p1.stdout.read()
    #             if stderr:
    #                 p1.kill()
    #                 raise Exception(f'执行命令{self.cmd}出错{stderr}')
    #
    #     log_thread = threading.Thread(target=run_cmd)
    #     log_thread.setDaemon(True)
    #     log_thread.start()


class AsyCmdFileTask(CmdBase):
    """
    执行测试命令类
    """

    def __init__(self, cmd, errFileFullPath=None, logFileFullPath=None):
        """
        初始化类
        :param cmd: 运行的命令
        :param errFileFullPath:
        :param logFileFullPath:
        :return:
        """
        super().__init__(cmd)
        if logFileFullPath:
            self.stdout = open(logFileFullPath, 'a+')
        if errFileFullPath:
            self.stderr = open(errFileFullPath, 'a+')
        self.my_timer = None

    # def stopCmdThread(self):
    #     try:
    #         if self._p:
    #             self.kill_process(self._p)
    #             self._p = None
    #         if self.my_timer and self.my_timer.is_alive():
    #             self.my_timer.cancel()
    #     except Exception as e:
    #         printe(traceback.format_exc())

    # def timeoutCallback(self, p):
    #     '''
    #     定时函数回调执行函数
    #     :param p: 进程
    #     :return:
    #     '''
    #     try:
    #         self.kill_process(p)
    #     except Exception as error:
    #         printe(traceback.format_exc())

    def _runCmd(self, timeout=None):
        self._p = subprocess.Popen(self._cmd, stdout=self.stdout.fileno(), stderr=self.stderr.fileno(), shell=True)
        # if timeout:
        #     self.my_timer = threading.Timer(timeout, self.timeoutCallback, [self._p])
        #     self.my_timer.start()
        printf("开始执行%s------pid:%d" % (self._cmd, self._p.pid))
        try:
            self._p.wait()
        except Exception:
            printe(traceback.format_exc())
        finally:
            if self.my_timer and self.my_timer.is_alive():
                self.my_timer.cancel()

    def startCmdThread(self, timeout=None):
        if self._p:
            self.stopTask()
        log_thread = threading.Thread(target=self._runCmd, args=(timeout,))
        log_thread.start()
        log_thread.setDaemon(True)
