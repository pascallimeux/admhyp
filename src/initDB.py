# -*- coding: utf-8 -*-
'''
Created on 28 june 2017
@author: pascal limeux
'''

from app.login.services import UserServices
from common.log import get_logger
logger = get_logger()

if __name__ == "__main__":
    userServices = UserServices()
    userServices.CreateDB()
    try:
        adm_username = "pascal"
        adm_password = "pascal"
        adm_email = "pascal.limeux@orange.com"
        user = userServices.CreateUser(username= adm_username, password=adm_password, email=adm_email)
        logger.info("Init DB with initial account admin: {0}/{1}".format(adm_username, adm_password))
    except Exception as e:
        logger.error("DB initialization failled: {}".format(e))

