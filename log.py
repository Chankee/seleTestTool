import logging
import os
import time

class Logger(object):
    def __init__(self,loggerName=None):
        if not os.path.exists("log"):
            os.mkdir("log")
        log_time = time.strftime("%Y-%m-%d")
        log_file = os.getcwd() + "/log" + "/" + log_time + ".log"

        # 创建文件 handler
        fh = logging.FileHandler(log_file, 'a', encoding='utf-8')
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        self.logger = logging.getLogger(loggerName)
        self.logger.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter(
            '[%(asctime)s] %(filename)s -->%(funcName)s line:%(lineno)d [%(levelname)s]  %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        fh.close()
        ch.close()
    def get_logger(self):
        return self.logger


# 初始化 日志实例
logger = Logger("SeRunner").get_logger()






