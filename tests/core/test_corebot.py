#!/usr/bin/env python
#coding=utf8

__author__ = 'liugang'

import unittest
import time
from wxbot.core.corebot import CoreBot

class TestCoreBot(unittest.TestCase):

    def setUp(self):
        self.corebot = CoreBot()
        print self.corebot.login()
        time.sleep(10)

    def test_login(self):
        print self.corebot.islogin()
        self.assertEqual(self.corebot.islogin(),True)

    def test_chat(self):
        self.corebot.choose_chat(u"有道抢红包")
        time.sleep(3)
        print self.corebot.get_current_chat()
        self.assertEqual(self.corebot.get_current_chat(), u"有道抢红包")
        self.corebot.choose_chat(u"吕丽")
        time.sleep(3)
        print self.corebot.get_current_chat()
        self.assertEqual(self.corebot.get_current_chat(), u"吕丽")

    def test_avatar(self):
        avatar = self.corebot._get_avatar()
        print avatar

    def test_get_msg(self):
        cnt = 0
        while True:
            time.sleep(10)
            msg_list = self.corebot.get_msg()
            for msg in msg_list:
                print msg
            print "-----------"
            cnt += 1
            if cnt > 10:
                break

    def test_send_msg(self):
        cnt = 0
        while True:
            time.sleep(10)
            self.corebot.send_msg("haha")
            cnt += 1
            if cnt > 10:
                break


if __name__ == "__main__":
    unittest.main()


