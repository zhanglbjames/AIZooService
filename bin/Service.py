#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import socket
from conf.setting import *
from ThreadPool import ThreadPool
from Job import SocketTask
from Chatbot import ChatModel

'''
@author zhanglbjames@163.com
Created 2017/5/8
'''


class Service(object):

    def __init__(self):
        self.__pool = ThreadPool()
        self.__chatModel = ChatModel()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((serverLocalHost, serverLocalPort))
        self.__socket = s

    def start_service(self):
        self.__socket.listen(10)
        while True:
            connection, address = self.__socket.accept()
            task = SocketTask(connection, address, self.__chatModel)
            self.__pool.execute(task)

    def stop_service(self):
        self.__pool.shutdown()
        self.__chatModel.close_resource()
        self.__socket.close()

