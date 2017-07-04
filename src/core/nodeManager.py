# -*- coding: utf-8 -*-
'''
Created on 26 june 2017
@author: pascal limeux
'''
from config import NodeType
import config, logging
from core.rcmd import CreateRemoteAdmin
from core.node import Peer, Orderer, Ca
from common.log import get_logger
logger = get_logger(__name__)

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class NodeManager(metaclass=Singleton):

    def InitRemoteLogin(self,hostname , password, username, pub_key_file ):
        CreateRemoteAdmin(hostname=hostname, password=password, username=username, pub_key_file=pub_key_file)


    def CreateCA(self, hostname, key_file=config.KEYFILE, remoteAdmin=config.USERADM):
        logger.info ("Create CA: {}".format(hostname))
        ca = Ca(hostname, key_file, NodeType.CA, remoteAdmin)
        return ca

    def CreateOrderer(self, hostname, key_file=config.KEYFILE, remoteAdmin=config.USERADM):
        logger.info ("Create ORDERER: {}".format(hostname))
        orderer = Orderer(hostname, key_file, NodeType.ORDERER, remoteAdmin)
        return orderer

    def CreatePeer(self, hostname, key_file=config.KEYFILE, remoteAdmin=config.USERADM):
        logger.info ("Create PEER: {}".format(hostname))
        peer = Peer(hostname, key_file, NodeType.PEER, remoteAdmin)
        return peer
