#!/usr/bin/env python
#coding=utf8

__author__ = 'liugang'

import time
from wxbot.client.client import WxbotClient
from wxbot.bean.bean import WxMsgShare

class ShareCollector(object):

    def __init__(self):
        self.wxclient = WxbotClient("http://localhost",8000)
        self.wxclient.logout("liuganglg")
        self.wxclient.create_wxbot("liuganglg")

    def share_collect(self,chat):
        self.wxclient.choose_chat("liuganglg","宋紫玫")
        while True:
            print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            msg_list = self.wxclient.get_msg("liuganglg")
            for msg in msg_list:
                if isinstance(msg, WxMsgShare):
                    print msg
            time.sleep(10)

def share_collect(chat):
    sc = ShareCollector()
    time.sleep(10)
    sc.share_collect(chat)


if __name__ == "__main__":
    share_collect("宋紫玫")
    # print time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    print "done"