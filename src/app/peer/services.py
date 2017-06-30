# -*- coding: utf-8 -*-
'''
Created on 30 june 2017
@author: pascal limeux
'''

from app.common.services import Services
from app.model import Peer
import logging
from common.log import LOG_LEVEL, log_handler
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)
from config import ServerType

class PeerServices(Services):

    def CreatePeer(self, hostname, login, key_file):
        try:
            peer = Peer(hostname=hostname, type=ServerType.PEER, login=login, key_file=key_file )
            self.__saveRecord(peer)
        except Exception as e:
            self.db_session.rollback()
            logger.error("{0}".format(e))
        return peer

    def RemovePeer(self, hostname):
        objs = self.db_session.query(Peer).filter(Peer.hostname==hostname)
        ret = objs.delete()
        self.db_session.commit()
        return ret

    def getPeer(self, hostname):
        return Peer.query.filter(Peer.hostname == hostname).first()

    def getPeers(self):
        return Peer.query.all()