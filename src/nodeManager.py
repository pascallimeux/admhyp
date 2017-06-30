# -*- coding: utf-8 -*-
'''
Created on 26 june 2017
@author: pascal limeux
'''
from config import NodeType
from common.log import LOG_LEVEL, log_handler
import config, logging
from node import Peer, Orderer, Ca
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class NodeManager(metaclass=Singleton):

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