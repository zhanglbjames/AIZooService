#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import threading
from Job import Task
from util.tools import Logger
'''
@author zhanglbjames@163.com
Created 2017/5/9
'''


'''
py 2.x 不支持内部嵌套类的相互调用
线程池工作线程对象
'''


class Worker(threading.Thread):
    def __init__(self, name, jobs, task_condition):
        # 必须显示调用父类的初始化函数
        super(Worker, self).__init__(name=name)
        self.__running = True
        self.jobs = jobs
        # task任务列表可重入锁条件变量
        self.task_condition = task_condition
        # running status lock
        self.__status_lock = threading.Lock()

    # 自定义的线程任务函数
    def run(self):
        job = None
        while self.__running:
            if self.task_condition.acquire():
                Logger.info(self.name + " acquire the task condition")
                # 如果此时任务列表为空，则一直等待
                while len(self.jobs) == 0:
                        self.task_condition.wait()
                # 任务列表不为空，则获取最后一个任务
                job = self.jobs.pop()

                # 通知等在task列表上的线程
                self.task_condition.notify()
                # 释放锁
                Logger.info(self.name + " release the task condition")
                self.task_condition.release()

            # 执行任务
            if isinstance(job, Task):
                Logger.info(self.name + " is doing task")
                job.do_task()

    def shutdown(self):
        self.__status_lock.acquire()
        try:
            self.__running = False
            Logger.info(self.name + " is stop")
        finally:
            self.__status_lock.release()





