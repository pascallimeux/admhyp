# -*- coding: utf-8 -*-
'''
Created on 6 july 2017
@author: pascal limeux
'''

from app.common.services import Services, ObjectNotFoundException
from app.orderer.model import Orderer
from app.database import get_session
from common.log import get_logger
logger = get_logger()
from app.common.constants import NodeType
from core.remotecommands import create_remote_admin, check_ssh_admin_connection

class OrdererServices(Services):

    def create_orderer(self, hostname, ca, remoteadmlogin, remotepassword, remotelogin, pub_key_file, key_file):
        try:
            create_remote_admin(hostname=hostname, password=remotepassword, username=remotelogin, pub_key_file=pub_key_file, adminusername=remoteadmlogin)
            if not check_ssh_admin_connection(hostname=hostname, remoteadminlogin=remoteadmlogin, key_file=key_file):
                raise Exception()
        except Exception as e:
            logger.error(e)
            raise Exception("Create remote admin failled!")
        try:
            orderer = Orderer(hostname=hostname, ca=ca, type=NodeType.ORDERER, login=remoteadmlogin, key_file=key_file )
            self.SaveRecord(orderer)
        except Exception as e:
            get_session().rollback()
            logger.error("{0}".format(e))
            raise Exception ("Data not record, database error!")

        return orderer

    def remove_orderer(self, hostname):
        objs = self.get_session().query(Orderer).filter(Orderer.hostname==hostname).filter(Orderer.type == NodeType.ORDERER)
        ret = objs.delete()
        get_session().commit()
        return ret

    def get_orderer(self, hostname):
        orderer = Orderer.query.filter(Orderer.hostname == hostname).filter(Orderer.type == NodeType.ORDERER).first()
        if orderer == None:
            raise ObjectNotFoundException()
        logger.debug(orderer)
        return orderer

    def get_orderers(self):
        return Orderer.query.filter(Orderer.type == NodeType.ORDERER)


    def stop(self, hostname):
        pass

    def start(self, hostname):
        pass

    def deploy(self, hostname):
        pass
