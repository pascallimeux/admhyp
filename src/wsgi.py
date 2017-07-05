# -*- coding: utf-8 -*-
'''
Created on 5 july 2017
@author: pascal limeux
'''

from app import app
from common.log import get_logger
logger = get_logger()

def user_is_logged_in():
    return True

if __name__ == "__main__":
    try:
        logger.info("Start application...")
        app.run()
    finally:
        logger.info("Stop application...")
