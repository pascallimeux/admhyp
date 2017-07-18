# -*- coding: utf-8 -*-
'''
Created on 30 june 2017
@author: pascal limeux
'''
from app.common.services import Services, ObjectNotFoundException
from app.ca.model import Ca
from app.database import get_session
from common.log import get_logger
logger = get_logger()
from app.common.constants import NodeType
from core.remotecommands import create_remote_admin, check_ssh_admin_connection

class CaServices(Services):

    def create_ca(self, hostname, remoteadmlogin, remotepassword, remotelogin, pub_key_file, key_file):
        try:
            create_remote_admin(hostname=hostname, password=remotepassword, username=remotelogin,
                                pub_key_file=pub_key_file, adminusername=remoteadmlogin)
            if not check_ssh_admin_connection(hostname=hostname, remoteadminlogin=remoteadmlogin, key_file=key_file):
                raise Exception()
        except Exception as e:
            logger.error(e)
            raise Exception("Create remote admin failled!")
        try:
            ca = Ca(hostname=hostname, type=NodeType.CA, login=remoteadmlogin, key_file=key_file)
            self.SaveRecord(ca)
        except Exception as e:
            get_session().rollback()
            logger.error("{0}".format(e))
            raise Exception("Data not record, database error!")
        return ca

    def remove_ca(self, hostname):
        objs = self.get_session().query(Ca).filter(Ca.hostname == hostname).filter( Ca.type == NodeType.CA)
        ret = objs.delete()
        get_session().commit()
        return ret

    def get_ca(self, hostname):
        ca = Ca.query.filter(Ca.hostname == hostname).filter( Ca.type == NodeType.CA).first()
        if ca == None:
            raise ObjectNotFoundException()
        logger.debug(ca)
        return ca

    def get_cas(self):
        return Ca.query.filter(Ca.type == NodeType.CA)

