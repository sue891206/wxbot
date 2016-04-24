#!/usr/bin/env python
#coding=utf8

__author__ = 'liugang'
import logging

class LoggerFactory(object):

    @staticmethod
    def get_logger(name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger