#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import threading
from conf.setting import *


'''
@author zhanglbjames@163.com
Created 2017/5/8
'''
class ThreadPool(object):
    def __init__(self,logger):
        self.__pool = []
        self.__tasks = []
        self.__results = {}
        self.__max_thread_num = threadPoolMaxNum
        self.__max_task_num = taskMaxNum
        self.__thread_count = 0
        self.__task_count = 0
        self.__logger = logger
        self.__lock = threading.Lock()
        self.__logger.info("create a Thread pool")

    # 添加任务
    def add_task(self, task):
        self.__lock.acquire()
        try:
            if self.__task_count > self.__max_task_num:
                self.__logger.warn("exceed the max_task_num, add failed")
                print "Info:exceed the max_task_num, add failed"
            else:
                self.__tasks.append(task)
                self.__task_count += 1
        finally:
            self.__lock.release()

    # 添加工作线程
    def add_worker(self):
        self.__lock.acquire()
        try:
            if self.__thread_count > self.__max_thread_num:
                self.__logger.warn("exceed the max_thread_num, add failed")
                print "Info:exceed the max_thread_num, add failed"
            else:
                thread = threading.Thread(target=)
                self.__pool.append(thread)
                self.__thread_count += 1
        finally:
            self.__lock.release()

    def excute(self):
        while True:
            task = None
            self.__lock.acquire()
            try:
                if len(self.__tasks) > 0:
                    self.__tasks.pop()

