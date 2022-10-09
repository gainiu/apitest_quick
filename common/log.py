'''
Author: xiaomin
Date: 2020-12-17 15:52:04
'''
import logging
import time
from config import file_path
import os
import sys
sys.path.append("..")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import colorama
colorama.init()

#创建一个logger，并设置log等级总开关INFO
logger=logging.getLogger()
logger.setLevel(logging.INFO)

def create_logfile(filename):
    #判断是否已存在log文件，不存在则新建
    if not os.path.isfile(filename):
        fd = open(filename,mode='a',encoding='utf-8')
        fd.close()
    else:
        pass

def set_handler(levels):
    #将logger添加到对应handler
    if levels==logging.ERROR:
        logger.addHandler(MyLog.err_handler)
    logger.addHandler(MyLog.console_handler)
    logger.addHandler(MyLog.handler)

def remove_handler(levels):
    if levels==logging.ERROR:
        logger.removeHandler(MyLog.err_handler)
    logger.removeHandler(MyLog.console_handler)
    logger.removeHandler(MyLog.handler)


class MyLog:
    '''封装日志'''
    #创建总日志文件和错误日志文件
    create_logfile(file_path.info_log)
    create_logfile(file_path.error_log)
    
    #创建3个handler用于写入日志文件，console_handler输出到控制台
    handler=logging.FileHandler(file_path.info_log,encoding='utf-8')
    err_handler=logging.FileHandler(file_path.error_log,encoding='utf-8')
    console_handler=logging.StreamHandler()
    
    #定义handler输出格式
    formatter=logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # errformatter=logging.Formatter('\033[31m%s\033[0m'%'%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    err_handler.setFormatter(formatter)
    

    @staticmethod
    def debug(log_message):
        #debug日志，调用logger添加handler方法，写入日志
        set_handler(logging.DEBUG)
        logger.debug(log_message)
        remove_handler(logging.DEBUG)

    @staticmethod
    def info(log_message):
        #info日志，调用logger添加handler方法，写入日志
        set_handler(logging.INFO)
        logger.info(log_message)
        remove_handler(logging.INFO)
    
    @staticmethod
    def warning(log_message):
        #warning日志，调用logger添加handler方法，写入日志
        set_handler(logging.WARNING)
        logger.warning(log_message)
        remove_handler(logging.WARNING)

    @staticmethod
    def error(log_message):
        #error日志，调用logger添加handler方法，写入日志
        set_handler(logging.ERROR)
        logger.error(log_message)
        remove_handler(logging.ERROR)
    
    @staticmethod
    def critical(log_message):
        #critical日志，调用logger添加handler方法，写入日志
        set_handler(logging.CRITICAL)
        logger.critical(log_message)
        remove_handler(logging.CRITICAL)

if __name__ == "__main__":
    MyLog.debug("This is debug message")
    MyLog.info("This is info message")
    MyLog.warning("This is warning message")
    MyLog.error("This is error message")
    MyLog.critical("This is critical message")