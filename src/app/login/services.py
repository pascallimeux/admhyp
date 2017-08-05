# -*- coding: utf-8 -*-
'''
Created on 30 june 2017
@author: pascal limeux
'''
from app.database import get_session
from app.common.services import Services
from app.login.model import User
from app.common.hashpwd import hash_password, check_password
from app.common.log import get_logger, log_function_call
logger = get_logger()
class UserServices(Services):

    @log_function_call
    def CreateUser(self, username, password, email):
        if username == None or password == None or email == None:
            raise MissingParametersException()
        user = User(email=email, username=username, password=hash_password(password))
        self.SaveRecord(user)
        logger.debug("Save new user(\"{}\")".format(username))
        return user

    @log_function_call
    def CheckUser(self, username, password):
        if username == None or password == None:
            raise MissingParametersException()
        rows = get_session().query(User).filter(User.username == username).count()
        if rows == 1:
            user = get_session().query(User).filter(User.username == username)[0]
            if check_password(user.password, password):
                return True
        return False

