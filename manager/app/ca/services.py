# -*- coding: utf-8 -*-
'''
Created on 30 june 2017
@author: pascal limeux
'''
from app.common.services import Services, ObjectNotFoundException
from app.ca.model import Ca
from app.database import get_session
from app.common.log import get_logger, log_function_call
logger = get_logger()
from app.common.constants import NodeType
from app.common.rcmds import create_remote_connection, check_ssh_admin_connection

class CaServices(Services):

    @log_function_call
    def create_ca(self, name, hostname, remoteadmlogin, remotepassword, remotelogin, pub_key_file, key_file):
        try:
            create_remote_connection(hostname=hostname, password=remotepassword, username=remotelogin,
                                pub_key_file=pub_key_file, adminusername=remoteadmlogin)
           # if not check_ssh_admin_connection(hostname=hostname, remoteadminlogin=remoteadmlogin, key_file=key_file):
           #     raise Exception()
        except Exception as e:
            logger.error(e)
            raise Exception("Create remote admin failled! {}".format(e))
        try:
            ca = Ca(name=name, hostname=hostname, type=NodeType.CA, login=remoteadmlogin, key_file=key_file)
            self.SaveRecord(ca)
        except Exception as e:
            get_session().rollback()
            logger.error("{0}".format(e))
            raise Exception("Data not record, database error!")
        return ca

    @log_function_call
    def remove_ca(self, name):
        objs = self.get_session().query(Ca).filter(Ca.name == name)
        ret = objs.delete()
        get_session().commit()
        return ret

    @log_function_call
    def get_ca(self, name):
        ca = Ca.query.filter(Ca.name == name).first()
        if ca == None:
            raise ObjectNotFoundException("no ca for name:{}".format(name))
        return ca

    @log_function_call
    def get_cas(self):
        return Ca.query.all()

