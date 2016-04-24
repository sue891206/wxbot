#!/usr/bin/env python
#coding=utf8

__author__ = 'liugang'

import SimpleXMLRPCServer,SocketServer
import xmlrpclib
import hashlib
import cPickle as pickle
import threading
from wxbot.core.corebot import CoreBot
from wxbot.utils.log_util import LoggerFactory


class WxbotService(object):
    def __init__(self):
        self.wxbot_dict = {}
        self.logger = LoggerFactory.get_logger(self.__class__.__name__)
        self.key_map = {}
        self.wx_mutex = threading.RLock()

    def __add_key_map(self,name):
        m = hashlib.md5()
        m.update(name)
        md5 = m.hexdigest()
        self.key_map[name] = md5
        self.key_map[md5] = name

    def __del_key_map(self,name):
        md5 = self.key_map[name]
        del self.key_map[name]
        del self.key_map[md5]

    def create_wxbot(self,name):
        self.logger.info("@@CREATE_WXBOT "+name)
        self.wx_mutex.acquire()
        if name in self.wxbot_dict:
            return None
        wxbot = CoreBot()
        self.wxbot_dict[name] = wxbot
        self.__add_key_map(name)
        self.wx_mutex.release()
        login_code = wxbot.login()
        return login_code

    def islogin(self,name):
        self.logger.info("@@IS_LOGIN " + name)
        if name in self.wxbot_dict:
            return self.wxbot_dict[name].islogin()
        else:
            return None

    def get_msg(self,name):
        self.logger.info("@@GET_MSG " + name)
        if name in self.wxbot_dict:
            return xmlrpclib.Binary(pickle.dumps(self.wxbot_dict[name].get_msg()))
        else:
            return None

    def send_msg(self,name,msg):
        self.logger.info("@@SEND_MSG " + name+": "+msg)
        if name in self.wxbot_dict:
            return self.wxbot_dict[name].send_msg(msg)
        else:
            return None

    def choose_chat(self,name,chat):
        self.logger.info("@@CHOOSE_CHAT " + name+"-> "+chat)
        if name in self.wxbot_dict:
            self.wxbot_dict[name].choose_chat(chat)

    def get_chat(self,name):
        self.logger.info("@@GET_CHAT " + name)
        if name in self.wxbot_dict:
            return self.wxbot_dict[name].get_chat()

    def logout(self,name):
        self.logger.info("@@LOGOUT " + name)
        if name in self.wxbot_dict:
            del self.wxbot_dict[name]
            self.__del_key_map(name)
            return True
        else:
            return False

    def logout_hash(self, hash):
        self.logger.info("@@LOGOUT_HASH " + hash)
        if hash in self.key_map:
            return self.logout(self.key_map[hash])
        else:
            return False

    def status(self):
        self.logger.info("@@STATUS")
        status_list = []
        for name in self.wxbot_dict:
            curbot = self.wxbot_dict[name]
            islogin = curbot.islogin()
            nickname = curbot._get_nickname()
            chat = curbot.get_chat()
            md5 = self.key_map[name]
            status_list.append((nickname,chat,islogin,md5))

        return status_list

class RPCThreading(SocketServer.ThreadingMixIn, SimpleXMLRPCServer.SimpleXMLRPCServer):
    pass

def wxbot_xmlrpc_service():
    rpc_instance = WxbotService()
    rpc_server = RPCThreading(("localhost",8000),allow_none=True)
    rpc_server.register_instance(rpc_instance)
    print "rpc server start"
    print rpc_server.system_listMethods()
    rpc_server.serve_forever()

if __name__ == "__main__":
    wxbot_xmlrpc_service()

