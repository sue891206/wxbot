#!/usr/bin/env python
#coding=utf8

__author__ = 'liugang'

import unittest
from wxbot.client.client import WxbotClient

class TestWxbotClient(unittest.TestCase):
    def setUp(self):
        self.client = WxbotClient("http://localhost", 8000)

    def test_status(self):
        status = self.client.get_status()
        print status
        for s in status:
            print s[0], s[1], s[2]

    def test_islogin(self):
        print self.client.islogin("liuganglg")

    @unittest.skip
    def test_create_wxbot(self):
        png = self.client.create_wxbot("liuganglg")
        with open("/Users/liugang/login.png", "wb") as fout:
            fout.write(png.data)

    @unittest.skip
    def test_logout(self):
        return self.client.logout("liuganglg")

    def test_get_chat(self):
        print self.client.get_chat("liuganglg")

    def test_send_msg(self):
        self.client.send_msg("liuganglg","你好Hello World")

    def test_get_msg(self):
        msg_list = self.client.get_msg("liuganglg")
        print msg_list
        for msg in msg_list:
            print msg

    def test_choose_chat(self):
        self.client.choose_chat("liuganglg","吕丽")


if __name__ == "__main__":
    unittest.main()