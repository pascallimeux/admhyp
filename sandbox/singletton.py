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
logger = get_logger()

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class NodeManager(metaclass=Singleton):

    def InitRemoteLogin(self,hostname , password, username, pub_key_file ):
        CreateRemoteAdmin(hostname=hostname, password=password, username=username, pub_key_file=pub_key_file)
