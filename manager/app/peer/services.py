# -*- coding: utf-8 -*-
'''
Created on 30 june 2017
@author: pascal limeux
'''

from app.common.services import Services, ObjectNotFoundException
from app.peer.model import Peer
from app.database import get_session
from app.common.log import get_logger, log_function_call
logger = get_logger()
from app.agent.agentBuilder import deploy_Agent
from app.common.constants import NodeType
from config import appconf


class PeerServices(Services):
    @log_function_call
    def create_peer(self, name, hostname, remotepassword, remoteadmlogin=appconf().USERADM,
                  remotelogin=appconf().REMOTEUSERNAME, pub_key_file=appconf().PUBKEYFILE, key_file=appconf().KEYFILE,
                  broker_address=appconf().BROKERADDRESS, deploy=True):
        if deploy:
            try:
                deploy_Agent(agent_name=hostname, password=remotepassword, hostname=hostname, login=remotelogin,
                             broker_address=broker_address, pub_key_file=pub_key_file)
            except Exception as e:
                logger.error(e)
                raise Exception("Deploy agent failled! {}".format(e))
        try:
            peer = Peer(name=name, hostname=hostname, type=NodeType.PEER, login=remoteadmlogin, key_file=key_file )
            self.SaveRecord(peer)
        except Exception as e:
            get_session().rollback()
            logger.error("{0}".format(e))
            raise Exception ("Data not created, database error!")
        return peer

    @log_function_call
    def remove_peer(self, name):
        objs = self.get_session().query(Peer).filter(Peer.name==name)
        ret = objs.delete()
        get_session().commit()
        return ret

    @log_function_call
    def get_peer(self, name):
        peer = Peer.query.filter(Peer.name == name).first()
        if peer == None:
            raise ObjectNotFoundException("no peer for name:{}".format(name))
        return peer

    @log_function_call
    def get_peers(self):
        return Peer.query.all()

    @log_function_call
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
