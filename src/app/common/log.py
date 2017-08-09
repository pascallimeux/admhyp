# -*- coding: utf-8 -*-
'''
Created on 28 june 2017
@author: pascal limeux
'''

import logging
from logging.handlers import RotatingFileHandler
from config import appconf
from functools import wraps

logger = None

def log_function_call(f):
    @wraps(f)
    def log (*args, **kwargs):
        logger.debug("Call function {0}({1})".format(f.__name__, str(kwargs)
                                                      .replace(":", "=")
                                                      .replace('\'', '')
                                                      .replace('{', '')
                                                      .replace('}','')
                                                      .replace(' ', '')))
        return f (*args, **kwargs)
    return log

def get_logger():
    global logger
    if logger is None:
        logger = configure_log()
    return logger


def configure_log():
    logger = logging.getLogger("admhyp")
    console_formatter = logging.Formatter('%(levelname)s\t%(pathname)s:%(lineno)d\t\t  %(asctime)s "%(message)s"')
    file_formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(pathname)s - l%(lineno)d - %(message)s', '%m-%d %H:%M:%S')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(appconf().LOG_LEVEL)
    console_handler.setFormatter(console_formatter)

    rotating_file_handler = RotatingFileHandler(appconf().LOGFILENAME, maxBytes=10000, backupCount=1)
    rotating_file_handler.setLevel(appconf().LOG_LEVEL)
    rotating_file_handler.setFormatter(file_formatter)

    if appconf().DEBUG:
        logger.addHandler(console_handler)
    logger.addHandler(rotating_file_handler)
    logger.setLevel(appconf().LOG_LEVEL)
    return logger
