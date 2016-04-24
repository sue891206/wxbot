#!/usr/bin/env python
#coding=utf8

__author__ = 'liugang'

class WxResponse(object):
    def __init__(self,code,msg,data):
        self.code = code
        self.msg = msg
        self.data = data

class WxMsg(object):
    def __init__(self,name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    def __str__(self):
        return "["+self.name+"]"

class WxMsgText(WxMsg):
    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self,text):
        self.__text = text

    def __str__(self):
        return "["+self.name+","+self.text+"]"

class WxMsgShare(WxMsg):
    @property
    def title(self):
        return self.__title
    @title.setter
    def title(self,title):
        self.__title = title

    @property
    def url(self):
        return self.__url
    @url.setter
    def url(self,url):
        self.__url = url

    def __str__(self):
        return "["+self.name+","+self.title+","+self.url+"]"

class WxMsgImg(WxMsg):
    @property
    def url(self):
        return self.__url
    @url.setter
    def url(self,url):
        self.__url = url

    def __str__(self):
        return "["+self.name+","+self.url+"]"

if __name__ == "__main__":
    wxtext = WxMsgText("lg")
    wxtext.text = "hello"
    print wxtext
    wxshare = WxMsgShare("szm")
    wxshare.title = "什么值得买"
    wxshare.url = "http://www.smzdm.com"
    print wxshare
    wximg = WxMsgImg("gtl")
    wximg.url = "http://xxx.com/haha.jpg"
    print wximg