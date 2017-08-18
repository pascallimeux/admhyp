# -*- coding: utf-8 -*-
'''
Created on 30 june 2017
@author: pascal limeux
'''

from app.common.services import Services, ObjectNotFoundException
from app.peer.model import Peer
from app.database import get_session
from app.common.log import get_logger
logger = get_logger()
from app.common.constants import NodeType
from app.common.rcmds import create_remote_connection, check_ssh_admin_connection


class PeerServices(Services):

    def create_peer(self, name, hostname, remoteadmlogin, remotepassword, remotelogin, pub_key_file, key_file):
        try:
            create_remote_connection(hostname=hostname, password=remotepassword, username=remotelogin, pub_key_file=pub_key_file, adminusername=remoteadmlogin)
            #if not check_ssh_admin_connection(hostname=hostname, remoteadminlogin=remoteadmlogin, key_file=key_file):
            #    raise Exception()
        except Exception as e:
            logger.error(e)
            raise Exception("Create remote admin failled!")
        try:
            peer = Peer(name=name, hostname=hostname, type=NodeType.PEER, login=remoteadmlogin, key_file=key_file )
            self.SaveRecord(peer)
        except Exception as e:
            get_session().rollback()
            logger.error("{0}".format(e))
            raise Exception ("Data not created, database error!")
        return peer

    def remove_peer(self, name):
        objs = self.get_session().query(Peer).filter(Peer.name==name)
        ret = objs.delete()
        get_session().commit()
        return ret

    def get_peer(self, name):
        peer = Peer.query.filter(Peer.name == name).first()
        if peer == None:
            raise ObjectNotFoundException("no peer for name:{}".format(name))
        return peer

    def get_peers(self):
        return Peer.query.all()

    def add_ca(self, name, ca):
        try:
            ca.register_node(nodename=name, password="pwd")
            ca.enroll_node(nodename=name, password="pwd")
            tgz = ca.get_msp(name=name)
            peer = self.get_peer(name)
            peer.set_msp(tgz, name)
            peer.ca = ca.id
            self.SaveRecord(peer)
        except Exception as e:
            get_session().rollback()
            logger.error("{0}".format(e))
            raise Exception("Data not update, database error!")
        return peer

