# -*- coding: utf-8 -*-
'''
Created on 28 june 2017
@author: pascal limeux
'''

import logging
from logging.handlers import RotatingFileHandler
from config import appconf


logger = None


def get_logger():
    global logger
    if logger == None:
        logger = configure_log()
    return logger

def configure_log():
    logger = logging.getLogger("admhyp")
    #formatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s] [%(filename)s:%(lineno)s %(funcName)20s()] - %(message)s")
    console_formatter = logging.Formatter('%(levelname)s\t%(filename)s:%(lineno)d\t\t  %(asctime)s "%(message)s"')
    file_formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(pathname)s - l%(lineno)d - %(message)s', '%m-%d %H:%M:%S')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(appconf().LOG_LEVEL)
    console_handler.setFormatter(console_formatter)

    rotatingfile_handler = RotatingFileHandler(appconf().LOGFILENAME, maxBytes=10000, backupCount=1)
    rotatingfile_handler.setLevel(appconf().LOG_LEVEL)
    rotatingfile_handler.setFormatter(file_formatter)

    if appconf().DEBUG:
        logger.addHandler(console_handler)
    logger.addHandler(rotatingfile_handler)
    logger.setLevel(appconf().LOG_LEVEL)
    return logger
