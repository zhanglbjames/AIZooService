#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import codecs
import os
import jieba
import jieba.analyse
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer
from whoosh.index import create_in
from whoosh.qparser import QueryParser
from extlib.textrank4zh import TextRank4Keyword
from datetime import datetime
import threading
from conf.setting import *
from util.tools import Logger
reload(sys)

'''
@author zhanglbjames@163.com
Created 2017/5/8
'''


class ChatModel(object):

    def __init__(self):
        # status: 0 - init object; 1 - finished file check; 2 - finished init chat model;
        # 3 - close all resource, wait to stop
        self.__status = 0
        self.__init_chat()
        self.__file_condition = threading.Condition()

    '''
    private method
    初始化所有资源及模型
    '''
    def __init_chat(self):
        self.__file_check()
        self.__init_model()

    '''
    public method
    关闭所有文件资源
    '''
    def close_resource(self):
        self.__questionLogFileObj.close()
        self.__status = 3

    '''
    public method
    返回当前模型状态
    '''
    def get_status(self):
        return self.__status

    '''
        public method
        获取问题的答案
        :param question
        :return content the answer content
    '''
    def get_answer(self, question):
        check_input_status = self.__check_input_question(question)
        if check_input_status == 1:
            return "你好像什么也没有说呀？！"
        if check_input_status == 2:
            return "你问的问题太短了！"
        if check_input_status == 0:
            answer = self.__get_model_answer(question)
            status, content = self.__check_output_answer(answer,question)
            return content

    '''
        private method
        检查所有文件资源
    '''

    def __file_check(self):
        try:
            self.__questionLogFileObj = codecs.open(questionLogFile, "a+", "utf-8")
        except IOError:
            Logger.error("cannot open log file，please check and try again")
            sys.exit(1)
        # tmp directory checkAndCheck
        try:
            if not os.path.exists(tmpDir):
                os.mkdir(tmpDir)
        except IOError:
            Logger.error("cannot make tmp directory，please check and try again")
            sys.exit(1)

        # open and read question-answer pair file
        if not os.path.exists(questionAnswerPairFile):
            Logger.error("cannot find questionAnswerPairFile file，please check and try again")
            sys.exit(1)

        self.__status = 1

    '''
        private method
        初始化chatbot模型
    '''
    def __init_model(self):
        analyzer = ChineseAnalyzer()
        schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True, analyzer=analyzer))
        ix = create_in(tmpDir, schema)
        writer = ix.writer()

        with codecs.open(questionAnswerPairFile, "a+", "utf-8") as _file:
            i = 0
            for line in _file:
                # print(line)
                i += 1
                writer.add_document(
                    title="line" + str(i),
                    path="/a",
                    content=line
                )

        writer.commit()
        self.__searcher = ix.searcher()
        self.__parser = QueryParser("content", schema=ix.schema)
        self.__status = 2

    '''
    private method
    获取输入问题的答案
        :param question the input string of question
        :return results the answer to the input question
    '''

    def __get_model_answer(self, question):
        tag1 = jieba.analyse.extract_tags(question, 3)
        tag2 = jieba.analyse.textrank(question, 3)
        keywords = []

        for tag in tag1:
            keywords.append(tag)
        for tag in tag2:
            if tag not in tag1:
                keywords.append(tag)

        tr4w = TextRank4Keyword()
        tr4w.analyze(text=question, lower=True, window=2)
        for item in tr4w.get_keywords(20, word_min_len=1):
            if item.word not in keywords:
                keywords.append(item.word)

        kstr = ""
        for k in keywords:
            if len(k) != 1:
                kstr = kstr + "AND" + k
            else:
                if k not in kstr:
                    kstr = kstr + "AND" + k
                    # print(k)
        estr = kstr[3:]
        print (estr)
        q = self.__parser.parse(estr)
        results = self.__searcher.search(q)
        return results

    '''
       private method
       检查输入问题的长度即内容
       :param question the input string of question
       :return boolean if the question is long enough, return True
       :return status the check status 0 means ok, 1 means null, 2 means not null but so short
    '''
    @staticmethod
    def __check_input_question(question):
        status = 0
        if len(question) == 0:
            Logger.error("Input question string is null")
            status = 1
            return status
        else:
            if len(question) < 8:
                Logger.error("Input question string is short than 8 characters")
                status = 2
                return status
        return status

    '''
        private method
        检查输出的答案
        :param answer the answer return by __get_model_answer()
        :return status the answer status 0 means have searched the answer, 1 means have not search the answer
        :return content the answer content
    '''

    def __check_output_answer(self, answer, question):
        status = 0
        if len(answer) == 0:
            content = "太难了，要不换个问法试试"
            status = 1
        else:
            #print answer[0]['content']
            content = str(answer[0]['content'].split(':')[1]).replace('u\'', '\'')
        now = datetime.now()

        while(True):
            if self.__file_condition.acquire():
                self.__questionLogFileObj.write("label[" + str(status) + "]"
                                                + now.strftime("%Y-%m-%d %H:%M:%S") + ":"
                                                + question
                                                + "\n")
                self.__file_condition.release()
                break

        return status, content

if __name__ == "__main__":
    print (sys.getdefaultencoding())
    chat = ChatModel()
    a_question = "大熊猫喜欢吃什么？"
    a_content = chat.get_answer(a_question)

    # content is utf-8
    print a_content
    while True:
        if chat.get_status() == 3:
            break
        chat.close_resource()
    Logger.info("close chatbot")