#!/usr/bin/env python
#coding=utf8

__author__ = 'liugang'

class WxUrlNormalize(object):
    HOST = "http://wx.qq.com"
    @staticmethod
    def fill_url_prefix(url):
        if url is None or url[0:4] == "http":
            return url
        else:
            return WxUrlNormalize.HOST+url
