# -*- coding: utf-8 -*-
'''
Created on 30 june 2017
@author: pascal limeux
'''

from sqlalchemy import Column, String, ForeignKey
from app.node.model import Node
from app.common.constants import NodeType
from common.log import get_logger
from common.commands import uncompress_msp
logger = get_logger()

class Peer(Node):
    __tablename__ = 'peer'
    id = Column(String, ForeignKey('node.hostname'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':NodeType.PEER,
    }
    ca = Column(String, ForeignKey("ca.id"))
    def get_type(self):
        return NodeType.PEER

    def set_msp(self, tgz, nodename):
        logger.debug("set_msp on node:{}".format(self.id))
        self.upload_file(tgz, "/var/hyperledger/msp.tgz")
        self.exec_command(uncompress_msp(nodename))
        logger.debug("{} msp is setting on: {}".format(self.id))