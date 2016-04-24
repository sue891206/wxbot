#!/usr/bin/env python
#coding=utf8

__author__ = 'liugang'
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import xmlrpclib
import cPickle as pickle

class WxbotClient(object):

    def __init__(self,host,port):
        self.server = xmlrpclib.ServerProxy(host+":"+str(port),allow_none=True)

    def get_status(self):
        return self.server.status()

    def create_wxbot(self,name):
        return self.server.create_wxbot(name)

    def islogin(self,name):
        return self.server.islogin(name)

    def get_msg(self,name):
        return pickle.loads(self.server.get_msg(name).data)

    def send_msg(self,name,msg):
        self.server.send_msg(name,msg)

    def choose_chat(self,name,chat):
        self.server.choose_chat(name,chat)

    def get_chat(self,name):
        return self.server.get_chat(name)

    def logout(self,name):
        return self.server.logout(name)

    def logout_hash(self,hash):
        return self.server.logout_hash(hash)



if __name__ == "__main__":
    pass