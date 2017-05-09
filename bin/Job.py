#!/usr/bin/python2.7
# -*- coding: utf-8 -*-


class Task(object):
    def do_task(self):
        pass


class SocketTask(Task):
    def __init__(self, socket, address, chat_model):
        super(SocketTask,self).__init__()
        self.__socket = socket
        self.__address = address
        self.__chatModel = chat_model

    def do_task(self):
        data = str(self.__socket.recv(1024))
        content = self.__chatModel.get_answer(data)
        self.__socket.send(content)


class TestTask(Task):
    def __init__(self, _list):
        super(TestTask,self).__init__()
        self.__list = _list

    def do_task(self):
        self.__list.append("h")