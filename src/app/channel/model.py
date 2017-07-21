# -*- coding: utf-8 -*-
'''
Created on 20 july 2017
@author: pascal limeux
'''

from sqlalchemy import Column, String, Date, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import datetime
from app.common.log import get_logger

logger = get_logger()

association_table_ca = Table('association_ca', Base.metadata,
    Column('channel_name', String, ForeignKey('channel.name'), primary_key=True),
    Column('ca_id', String, ForeignKey('ca.id'), primary_key=True)
)
association_table_orderer = Table('association_orderer', Base.metadata,
    Column('channel_name', String, ForeignKey('channel.name'), primary_key=True),
    Column('orderer_id', String, ForeignKey('orderer.id'), primary_key=True)
)
association_table_peer = Table('association_peer', Base.metadata,
    Column('channel_name', String, ForeignKey('channel.name'), primary_key=True),
    Column('peer_id', String, ForeignKey('peer.id'), primary_key=True)
)

class Channel(Base):
    __tablename__ = 'channel'
    name = Column(String, primary_key=True)
    cas  = relationship("Ca", secondary=association_table_ca)
    orderers = relationship("Orderer", secondary=association_table_orderer)
    peers = relationship("Peer", secondary=association_table_peer)
    created = Column(Date(), default=datetime.date.today())


