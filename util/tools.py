#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from datetime import datetime
import threading

'''
@author zhanglbjames@163.com
Created 2017/5/9
'''


class Logger(object):

    # 类打印输出重入锁条件变量
    print_condition = threading.Condition()

    # 私有静态公共方法
    @staticmethod
    def __print_content(level, content):
        now = datetime.now()
        text = now.strftime("[%Y-%m-%d %H:%M:%S]")+level+":"+content
        # python print 函数默认换行，但是其他的写入文件的操作需要添加换行符
        if Logger.print_condition.acquire():
            print text
            Logger.print_condition.release()

    @staticmethod
    def info(content):
        Logger.__print_content("Info", content)

    @staticmethod
    def warning(content):
        Logger.__print_content("Warning", content)

    @staticmethod
    def error(content):
        Logger.__print_content("Error", content)

if __name__ == "__main__":
    Logger.info("不错")
    Logger.error("不错")
    Logger.warning("不错")