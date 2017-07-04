# -*- coding: utf-8 -*-
'''
Created on 30 june 2017
@author: pascal limeux
'''

from app.common.services import Services
from app.model import Ca
from common.log import get_logger
logger = get_logger(__name__)
from config import ServerType

class CaServices(Services):

    def CreateCa(self, hostname, login, key_file):
        try:
            ca = Ca(hostname=hostname, type=ServerType.CA, login=login, key_file=key_file )
            self.__saveRecord(ca)
        except Exception as e:
            self.db_session.rollback()
            logger.error("{0}".format(e))
        return ca

    def RemoveCa(self, hostname):
        objs = self.db_session.query(Ca).filter(Ca.hostname==hostname)
        ret = objs.delete()
        self.db_session.commit()
        return ret

    def getCa(self, hostname):
        return Ca.query.filter(Ca.hostname == hostname).first()

    def getCa(self):
        return Ca.query.all()
