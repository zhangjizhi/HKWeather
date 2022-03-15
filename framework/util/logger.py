# _*_ coding: utf-8 _*
import sys
import logging
import time
import datetime
from logging.handlers import RotatingFileHandler

__all__ = [
    'printf',
    'printe',
    'printw',
]


'''
日志配置
'''
# import logging.config
# import  os
# path = os.path.dirname(__file__)
# CONF_LOG = os.path.join(path,'log.ini')
# logging.config.fileConfig(CONF_LOG)
# Log = logging.getLogger('AutoTest')


class LogFormatter(logging.Formatter):

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = time.strftime(datefmt, ct)
        else:
            # t = time.strftime(self.default_time_format, ct)
            # s = self.default_msec_format % (t, record.msecs)
            s = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        return s


class LogStreamHandler(logging.StreamHandler):

    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            if record.levelno == logging.WARNING:
                msg = '\033[0;33m' + msg + self.terminator + '\033[0m'
            elif record.levelno == logging.ERROR:
                msg = '\033[0;31m' + msg + self.terminator + '\033[0m'
            else:
                msg = msg + self.terminator
            stream.write(msg)
            self.flush()
        except RecursionError:  # See issue 36272
            raise
        except Exception:
            self.handleError(record)


class Logger:

    logger = logging.getLogger('log')
    logger.setLevel(logging.INFO)

    @staticmethod
    def addFileHandler(file_path):
        file_handler = RotatingFileHandler(file_path, maxBytes=10 * 1024)
        logformatter = LogFormatter('[%(asctime)s][%(levelname)0.1s]%(message)s')
        file_handler.setFormatter(logformatter)
        Logger.logger.addHandler(file_handler)

    def removeFileHandler(self, file_path):
        for handle in self.logger.handlers:
            base_filename = getattr(handle, 'baseFilename', None)
            if base_filename == file_path:
                self.logger.removeHandler(handle)

    def addStreamHandler(self):
        stream_handler = LogStreamHandler(sys.stdout)
        logformatter = LogFormatter('[%(asctime)s][%(levelname)0.1s]%(message)s')
        stream_handler.setFormatter(logformatter)
        self.logger.addHandler(stream_handler)

    @staticmethod
    def getSysFrame(msg):
        f_back = sys._getframe().f_back.f_back.f_back
        msg = "[%s.%s]:%s" % (f_back.f_code.co_name, f_back.f_lineno, msg)
        return msg

    def printf(self, msg, trace):
        if trace:
            msg = self.getSysFrame(msg)
        self.logger.info(msg)

    def printw(self, msg, trace):
        if trace:
            msg = self.getSysFrame(msg)
        self.logger.warning(msg)

    def printe(self, msg, trace):
        if trace:
            msg = self.getSysFrame(msg)
        self.logger.error(msg)


logger = Logger()
logger.addStreamHandler()


def printf(msg, trace=True):
    logger.printf(msg, trace)


def printw(msg, trace=True):
    logger.printw(msg, trace)


def printe(msg, trace=True):
    logger.printe(msg, trace)


if __name__ == '__main__':
    printf('printf')
    printw('printw')
    printe('printe')
