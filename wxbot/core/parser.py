#!/usr/bin/env python
#coding=utf8

__author__ = 'liugang'

import time
from urllib import unquote
import re
from selenium.common.exceptions import NoSuchElementException
from wxbot.utils.url_util import WxUrlNormalize
from wxbot.bean.bean import WxMsgText,WxMsgShare

class WxWebParser(object):
    ACTION_INTERVAL = 3
    REGEX_SHARE_URL = re.compile(r".*requrl=(http[^&]*).*")

    @staticmethod
    def get_nickname(wxdriver):
        try:
            nickname_ele = wxdriver.find_element_by_xpath("//h3[@class='nickname']/span")
            return nickname_ele.text
        except NoSuchElementException,e:
            return None

    @staticmethod
    def get_avatar(wxdriver):
        try:
            avatar_ele = wxdriver.find_element_by_xpath("//div[@class='avatar']/img")
            return WxUrlNormalize.fill_url_prefix(avatar_ele.get_attribute("src"))
        except NoSuchElementException, e:
            return None

    @staticmethod
    def choose_chat(wxdriver,chat):
        try:
            input_ele = wxdriver.find_element_by_xpath("//div[@class='search_bar']/input")
            input_ele.clear()
            input_ele.send_keys(chat)
            time.sleep(WxWebParser.ACTION_INTERVAL)
            chat_list_ele = wxdriver.find_element_by_xpath("//div[@class='contact_item on']")
            chat_list_ele.click()
        except Exception,e:
            print e

    @staticmethod
    def get_current_chat(wxdriver):
        try:
            chat_ele = wxdriver.find_element_by_xpath("//div[@class='title poi']/a")
            return chat_ele.text
        except NoSuchElementException,e:
            return None

    @staticmethod
    def get_msg(wxdriver):
        """get current chat message list(only return latest 10 messages)
        :param wxdriver:
        :return wxmsg_list: current chat message list(receive message).
        """
        msg_list = []
        try:
            msg_ele_list = wxdriver.find_elements_by_xpath("//div[@class='message ng-scope you']")
            for msg_ele in msg_ele_list:
                msg = WxWebParser.package_text(msg_ele)
                if msg is None:
                    msg = WxWebParser.package_share(msg_ele)
                if msg is None:
                    msg = WxWebParser.package_img(msg_ele)
                if msg is not None:
                    msg_list.append(msg)
        except NoSuchElementException,e:
            print e
        return msg_list

    @staticmethod
    def _get_publisher_name(msg_ele):
        try:
            name_ele = msg_ele.find_element_by_xpath("./img")
            if name_ele is not None:
                name = name_ele.get_attribute("title")
                return name
            return None
        except NoSuchElementException,e:
            print e
            return None

    @staticmethod
    def _get_img(msg_ele):
        pass

    @staticmethod
    def _get_text(msg_ele):
        try:
            text_ele = msg_ele.find_element_by_xpath(".//div[@class='plain']/pre")
            if text_ele is not None:
                return text_ele.text
            return None
        except NoSuchElementException, e:
            print e
            return None

    @staticmethod
    def _get_share_title(msg_ele):
        try:
            title_ele = msg_ele.find_element_by_xpath(".//h4[@class='title ng-binding']")
            if title_ele is not None:
                return title_ele.text
            return None
        except NoSuchElementException, e:
            print e
            return None

    @staticmethod
    def _get_share_url(msg_ele):
        try:
            url_ele = msg_ele.find_element_by_xpath(".//div[@class='bubble_cont primary ng-scope']/a")
            if url_ele is not None:
                ng_url = url_ele.get_attribute("ng-href")
                m = WxWebParser.REGEX_SHARE_URL.match(ng_url)
                if m:
                    url = unquote(m.group(1))
                    return url
            return None
        except NoSuchElementException, e:
            return None

    @staticmethod
    def package_text(msg_ele):
        name = WxWebParser._get_publisher_name(msg_ele)
        text = WxWebParser._get_text(msg_ele)
        if name is None or text is None:
            return None
        else:
            msg = WxMsgText(name)
            msg.text = text
            return msg

    @staticmethod
    def package_share(msg_ele):
        name = WxWebParser._get_publisher_name(msg_ele)
        title = WxWebParser._get_share_title(msg_ele)
        url = WxWebParser._get_share_url(msg_ele)
        if name is None or title is None or url is None:
            return None
        else:
            msg = WxMsgShare(name)
            msg.title = title
            msg.url = url
            return msg

    @staticmethod
    def package_img():
        return None


    @staticmethod
    def send_msg(wxdriver,message):
        if isinstance(message,str):
            message = message.decode("utf8")
        try:
            input_ele = wxdriver.find_element_by_id("editArea")
            input_ele.send_keys(message)
            send_ele = wxdriver.find_element_by_class_name("btn_send")
            send_ele.click()
        except Exception,e:
            print e
            print "send message error"

    @staticmethod
    def get_qrcode_url(wxdriver):
        qrcode_ele = wxdriver.find_element_by_xpath("//div[@class='qrcode']/img")
        if qrcode_ele is not None:
            url = qrcode_ele.get_attribute("src")
            return url
        return None