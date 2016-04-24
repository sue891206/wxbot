#!/usr/bin/env python
#coding=utf8

__author__ = 'liugang'

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time
from selenium import webdriver
from wxbot.core.parser import WxWebParser

class Bot(object):
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self,name):
        self.__name = name

class CoreBot(Bot):

    LOGIN_URL = "https://wx.qq.com/"

    def login(self):
        self.wxdriver = webdriver.Chrome("/Users/liugang/Documents/PycharmProjects/smzdm/chromedriver")
        self.wxdriver.get(CoreBot.LOGIN_URL)
        url = WxWebParser.get_qrcode_url(self.wxdriver)
        return url

    def islogin(self):
        nickname = self._get_nickname()
        if nickname is None or len(nickname) == 0:
            return False
        else:
            return True

    def get_msg(self):
        return WxWebParser.get_msg(self.wxdriver)

    def send_msg(self,message):
        WxWebParser.send_msg(self.wxdriver,message)

    def choose_chat(self,chat):
        WxWebParser.choose_chat(self.wxdriver,chat)

    def get_chat(self):
        return WxWebParser.get_current_chat(self.wxdriver)

    def _get_nickname(self):
        return WxWebParser.get_nickname(self.wxdriver)

    def _get_avatar(self):
        return WxWebParser.get_avatar(self.wxdriver)

    def __del__(self):
        self.wxdriver.quit()

if __name__ == "__main__":
    cb = CoreBot("lg")
    cb.login()
    time.sleep(10)
    print cb.islogin()
    # time.sleep(10)
    # cb.choose_chat(u"宋紫玫")
    # time.sleep(10)
    # print "chat is",cb.get_current_chat()
    # cb.send_msg("Hello Wrold!新园区")
    # time.sleep(10)
    for i in xrange(100):
        msg_ele_list = cb.get_msg()
        print len(msg_ele_list)
        time.sleep(5)
