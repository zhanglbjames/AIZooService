#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import socket

'''
@author zhanglbjames@163.com
Created 2017/5/9
'''

'''
socket 客户端测试程序
'''
if __name__ == "__main__":

    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect(("localhost", 9034))
    socket.send("大熊猫喜欢吃什么东西？")
    data = str(socket.recv(1024))
    print data.decode("utf8")
    socket.close()