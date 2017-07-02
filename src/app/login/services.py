# -*- coding: utf-8 -*-
'''
Created on 30 june 2017
@author: pascal limeux
'''
from app.database import get_session
from app.common.services import Services
from app.login.model import User
from common.log import logging
logger = logging.getLogger(__name__)
from app.common.hashpwd import hash_password, check_password

class UserServices(Services):

    def CreateUser(self, username, password, email):
        if username == None or password == None or email == None:
            raise MissingParametersException()
        user = User(email=email, username=username, password=hash_password(password))
        self.SaveRecord(user)
        return user


    def CheckUser(self, username, password):
        if username == None or password == None:
            raise MissingParametersException()
        rows = get_session().query(User).filter(User.username == username).count()
        if rows == 1:
            user = get_session().query(User).filter(User.username == username)[0]
            if check_password(user.password, password):
                return True
        return False

