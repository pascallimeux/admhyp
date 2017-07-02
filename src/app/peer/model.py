# -*- coding: utf-8 -*-
'''
Created on 30 june 2017
@author: pascal limeux
'''

from sqlalchemy import Column, String, ForeignKey, Date
from app.node.model import Node
from app.common.constants import NodeType

class Peer(Node):
    __tablename__ = 'peer'
    id = Column(String, ForeignKey('node.hostname'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':NodeType.PEER,
    }
