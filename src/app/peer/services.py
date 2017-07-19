# -*- coding: utf-8 -*-
'''
Created on 30 june 2017
@author: pascal limeux
'''

from app.common.services import Services, ObjectNotFoundException
from app.peer.model import Peer
from app.database import get_session
from common.log import get_logger
logger = get_logger()
from app.common.constants import NodeType
from core.remotecommands import create_remote_connection, check_ssh_admin_connection
from app.ca.services import CaServices


class PeerServices(Services):

    def create_peer(self, hostname, remoteadmlogin, remotepassword, remotelogin, pub_key_file, key_file):
        try:
            create_remote_connection(hostname=hostname, password=remotepassword, username=remotelogin, pub_key_file=pub_key_file, adminusername=remoteadmlogin)
            if not check_ssh_admin_connection(hostname=hostname, remoteadminlogin=remoteadmlogin, key_file=key_file):
                raise Exception()
        except Exception as e:
            logger.error(e)
            raise Exception("Create remote admin failled!")
        try:
            peer = Peer(hostname=hostname, type=NodeType.PEER, login=remoteadmlogin, key_file=key_file )
            self.SaveRecord(peer)
        except Exception as e:
            get_session().rollback()
            logger.error("{0}".format(e))
            raise Exception ("Data not created, database error!")

        return peer

    def remove_peer(self, hostname):
        objs = self.get_session().query(Peer).filter(Peer.hostname==hostname).filter(Peer.type == NodeType.PEER)
        ret = objs.delete()
        get_session().commit()
        return ret

    def get_peer(self, hostname):
        peer = Peer.query.filter(Peer.hostname == hostname).filter(Peer.type == NodeType.PEER).first()
        if peer == None:
            raise ObjectNotFoundException()
        logger.debug(peer)
        return peer

    def get_peers(self):
        return Peer.query.filter(Peer.type == NodeType.PEER)

    def add_ca(self, hostname, ca_id):
        try:
            peer = self.get_peer(hostname)
            peer.ca = ca_id
            self.SaveRecord(peer)
        except Exception as e:
            get_session().rollback()
            logger.error("{0}".format(e))
            raise Exception("Data not update, database error!")
        return peer