#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import threading
from conf.setting import *
import types

# 从Worker模块 导入Worker对象
from Worker import Worker
from Job import Task
from util.tools import Logger

import time

'''
@author zhanglbjames@163.com
Created 2017/5/8
'''

'''
线程池：初始化指定数量的线程，当有任务列表的数量大于默认数量的线程时，
则每新增的大于默认的将启动一个新的线程执行，直到达到最大线程数，线程数将自增不减
'''


class ThreadPool(object):
    def __init__(self):
        self.__pool = []
        self.__tasks = []
        self.__max_thread_num = threadPoolMaxNum
        self.__max_task_num = taskMaxNum
        self.__default_thread_num = defaultThreadNum
        # 任务列表的可重入锁条件变量
        self.__task_condition = threading.Condition()
        # 线程池列表的可重入锁条件变量
        self.__pool_condition = threading.Condition()

        Logger.info("create a Thread pool")
        # 初始化工作线程
        self.__init_workers()
        Logger.info("init workers finished")

    # public method : 执行输入的任务
    def execute(self, task):
        if isinstance(task, Task):
            # 只要在新任务没有添加之前就已经超负荷了，则先立马新增线程，然后再添加任务
            # 这里没有加锁，因为这只是对系统负荷的一种粗略估计，不需要确切的数值
            if len(self.__tasks) >= len(self.__pool):
                self.__add_worker()
            self.__add_task(task=task)

    # public method : 将所有工作线程设置为关闭状态
    def shutdown(self):
        for worker in self.__pool:
            worker.shutdown()
        Logger.info("shutdown thread pool")

    # private method ：初始化默认数量的线程数
    def __init_workers(self):
        for i in range(defaultThreadNum):
            worker = Worker(name="worker_" + str(i+1), jobs=self.__tasks, task_condition=self.__task_condition)
            self.__pool.append(worker)
            worker.start()
            self.__thread_count = defaultThreadNum

    # private method ：添加任务
    def __add_task(self, task):
        self.__task_condition.acquire()
        try:
            if len(self.__tasks) > self.__max_task_num:
                Logger.info("exceed the max_task_num, add failed")
                self.__pool_condition.wait()
            else:
                # 将任务插入列表头
                self.__tasks.insert(0, task)
                Logger.info("added a task")
                # 添加任务，则唤醒等待的线程
                self.__task_condition.notify()

        finally:
            self.__task_condition.release()

    # private method :添加工作线程
    def __add_worker(self):
        self.__pool_condition.acquire()
        try:
            if len(self.__pool) > self.__max_thread_num:
                Logger.info("exceed the max_thread_num, add failed")
                self.__pool_condition.wait()
            else:
                worker = Worker(name="worker_" + str(len(self.__pool)+1), jobs=self.__tasks, task_condition=self.__task_condition)
                self.__pool.append(worker)
                Logger.info("add a worker_"+ str(len(self.__pool)+1))
                worker.start()
                self.__pool_condition.notify()
        finally:
            self.__pool_condition.release()


if __name__ == "__main__":
    pool = ThreadPool()

    count = 0

    def print_text(count = count):
        count += 1

    for i in range(100):
        pool.execute(print_text)
    time.sleep(3)
    print count