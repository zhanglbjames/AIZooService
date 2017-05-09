#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import socket
import threading
from conf.setting import *

'''
@author zhanglbjames@163.com
Created 2017/5/8
'''

class ServicePool(object):

    def __init__(self):
        self.__status = 0

    def __init_server(self):
        # init socket connections
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind(serverLocalHost,serverLocalPort)
        s.listen(10)
        self.__socket = s
        # init Thread pool