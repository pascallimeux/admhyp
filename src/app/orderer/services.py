# -*- coding: utf-8 -*-
'''
Created on 30 june 2017
@author: pascal limeux
'''

from app.common.services import Services
from app.model import Orderer
from common.log import get_logger
logger = get_logger(__name__)
from config import ServerType

class OrdererServices(Services):

    def CreateOrderer(self, hostname, login, key_file):
        try:
            orderer = Orderer(hostname=hostname, type=ServerType.ORDERER, login=login, key_file=key_file )
            self.__saveRecord(ca)
        except Exception as e:
            self.db_session.rollback()
            logger.error("{0}".format(e))
        return orderer

    def RemoveOrderer(self, hostname):
        objs = self.db_session.query(Orderer).filter(Orderer.hostname==hostname)
        ret = objs.delete()
        self.db_session.commit()
        return ret

    def getOrderer(self, hostname):
        return Orderer.query.filter(Orderer.hostname == hostname).first()

    def getOrderer(self):
        return Orderer.query.all()
