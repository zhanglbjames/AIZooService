#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import logging

'''
@author zhanglbjames@163.com
Created 2017/5/8
'''
# chat bot settings
questionLogFile = "../resource/question.log"
questionAnswerPairFile = "../resource/questionAnswer.pair"
tmpDir = "../resource/tmp/"
loggingFile = "../resource/info.log"


 # set logging
logger = logging.basicConfig(level=logging.INFO,
                                format="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s",
                                datefmt="%Y-%m-%d %H:%M:%S",
                                filename=loggingFile,
                                filemode="a+")

# server settings
serverLocalHost = "127.0.0.1"
serverLocalPort = "8888"

threadPoolMaxNum = 10
taskMaxNum = 10

