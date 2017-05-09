#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import logging

'''
@author zhanglbjames@163.com
Created 2017/5/8
'''
# chat bot settings
'''
路径位置以最开始的主程序的路径为相对位置
'''
questionLogFile = "resource/question.log"
questionAnswerPairFile = "resource/questionAnswer.pair"
tmpDir = "resource/tmp/"
loggingFile = "resource/info.log"


 # set logging



# server settings
serverLocalHost = "localhost"
serverLocalPort = 8888

threadPoolMaxNum = 10
taskMaxNum = 10
defaultThreadNum = 5

'''
logger = logging.basicConfig(level=logging.INFO,
                                format="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s",
                                datefmt="%Y-%m-%d %H:%M:%S",
                                filename=loggingFile,
                                filemode="a+")
'''