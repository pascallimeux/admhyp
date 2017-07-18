# -*- coding: utf-8 -*-
'''
Created on 7 july 2017
@author: pascal limeux
'''

from sqlalchemy import Column, String, ForeignKey
from app.node.model import Node
from app.common.constants import NodeType

class Orderer(Node):
    __tablename__ = 'orderer'
    id = Column(String, ForeignKey('node.hostname'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':NodeType.ORDERER,
    }
    ca = Column(String, ForeignKey("ca.id"))

    def get_type(self):
        return NodeType.ORDERER