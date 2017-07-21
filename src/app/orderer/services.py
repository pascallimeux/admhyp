# -*- coding: utf-8 -*-
'''
Created on 6 july 2017
@author: pascal limeux
'''

from app.common.services import Services, ObjectNotFoundException
from app.orderer.model import Orderer
from app.database import get_session
from app.common.log import get_logger
logger = get_logger()
from app.common.constants import NodeType
from app.common.rcmds import create_remote_connection, check_ssh_admin_connection

class OrdererServices(Services):

    def create_orderer(self, name, hostname, remoteadmlogin, remotepassword, remotelogin, pub_key_file, key_file):
        try:
            create_remote_connection(hostname=hostname, password=remotepassword, username=remotelogin, pub_key_file=pub_key_file, adminusername=remoteadmlogin)
            #if not check_ssh_admin_connection(hostname=hostname, remoteadminlogin=remoteadmlogin, key_file=key_file):
            #    raise Exception()
        except Exception as e:
            logger.error(e)
            raise Exception("Create remote admin failled!")
        try:
            orderer = Orderer(name=name, hostname=hostname, type=NodeType.ORDERER, login=remoteadmlogin, key_file=key_file )
            self.SaveRecord(orderer)
        except Exception as e:
            get_session().rollback()
            logger.error("{0}".format(e))
            raise Exception ("Data not record, database error!")

        return orderer

    def remove_orderer(self, name):
        objs = self.get_session().query(Orderer).filter(Orderer.name==name)
        ret = objs.delete()
        get_session().commit()
        return ret

    def get_orderer(self, name):
        orderer = Orderer.query.filter(Orderer.name == name).first()
        if orderer == None:
            raise ObjectNotFoundException()
        return orderer

    def get_orderers(self):
        return Orderer.query.all()


    def add_ca(self, name, ca):
        try:
            ca.register_node(nodename=name, password="pwd")
            ca.enroll_node(nodename=name, password="pwd")
            tgz = ca.get_msp(name=name)
            orderer = self.get_orderer(name)
            orderer.set_msp(tgz, name)
            orderer.ca = ca.id
            self.SaveRecord(orderer)
        except Exception as e:
            get_session().rollback()
            logger.error("{0}".format(e))
            raise Exception("Data not update, database error!")
        return orderer