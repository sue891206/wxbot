#!/usr/bin/env python
#coding=utf8

__author__ = 'liugang'
import simplejson as json
import tornado.ioloop
import tornado.web
import tornado.autoreload
from tornado.options import define, options
from wxbot.client.client import WxbotClient
from wxbot.utils.log_util import LoggerFactory
from wxbot.conf.config import *

define("port", default=8001, help="run on the given port", type=int)
define("rpcserver", default="http://localhost", help="rpc server host")
define("rpcport", default=8000, help="rpc server port", type=int)
define("debug", default=True, help="Debug Mode", type=bool)

settings = {
    "debug":options.debug
}

class AbstractWxbotHandler(tornado.web.RequestHandler):

    def initialize(self, client):
        self.client = client
        self.logger = LoggerFactory.get_logger(self.__class__.__name__)

class MainHandler(AbstractWxbotHandler):

    def get(self):
        status_list = self.client.get_status()
        sts_list = []
        for status in status_list:
            sts = {}
            sts["name"] = status[0]
            sts["chat"] = status[1]
            sts["login"] = status[2]
            sts_list.append(sts)

        self.render("index.html", sts_list = sts_list)

class StatusHandler(AbstractWxbotHandler):

    def get(self):
        self.logger.info("@@GET_STATUS")
        status_list = self.client.get_status()
        sts_list = []
        for status in status_list:
            sts = {}
            sts["name"] = status[0]
            sts["chat"] = status[1]
            sts["login"] = status[2]
            sts_list.append(sts)
        self.write(json.dumps(sts_list))


class CreateHandler(AbstractWxbotHandler):

    def get(self,name):
        res= {}
        login_code = self.client.create_wxbot(name)
        if login_code is None:
            res["code"] = 1
            res["msg"] = "Already Login"
        else:
            res["code"] = 0
            res["png"] = login_code

        self.write(json.dumps(res))

class LogoutHandler(AbstractWxbotHandler):

    def get(self,name):
        res = {}
        logout = self.client.logout(name)
        if logout:
            res["code"] = 0
            res["msg"] = "OK"
        else:
            res["code"] = 1
            res["msg"] = "Error"
        self.write(json.dumps(res))

class LogoutHashHandler(AbstractWxbotHandler):

    def get(self,hash):
        res = {}
        logout = self.client.logout_hash(hash)
        if logout:
            res["code"] = 0
            res["msg"] = "OK"
        else:
            res["code"] = 1
            res["msg"] = "Error"
        self.write(json.dumps(res))

def start_wxbot_web():
    client = WxbotClient(options.rpcserver,options.rpcport)
    app = tornado.web.Application([
        (r"/wxbot/status", StatusHandler,dict(client=client)),
        (r"/wxbot/create/(\w+)", CreateHandler, dict(client=client)),
        (r"/wxbot/logout/(\w+)", LogoutHandler, dict(client=client)),
        (r"/wxbot/logouthash/(\w+)", LogoutHashHandler, dict(client=client)),
        (r"/wxbot/monitor", MainHandler, dict(client=client)),
    ],template_path=WEB_TEMPLATE,static_path=WEB_STATIC,**settings)
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    start_wxbot_web()





