# -*- coding: utf-8 -*-
'''
Created on 28 june 2017
@author: pascal limeux
'''
from app.database import init_db
from common.log import LOG_LEVEL, log_handler
import config, logging, json
from app.login.services import UserServices
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)

if __name__ == "__main__":
    userServices = UserServices()
    userServices.CreateDB()
    try:
        adm_username = "pascal"
        adm_password = "pascal"
        adm_email = "pascal.limeux@orange.com"
        user = userServices.CreateUser(username= adm_username, password=adm_password, email=adm_email)
        logger.info("Init DB with initial admin account: {0}".format(user.username))
    except Exception as e:
        logger.error("DB initialization failled: {}".format(e))

