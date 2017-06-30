# -*- coding: utf-8 -*-
'''
Created on 27 june 2017
@author: pascal limeux
'''
from sqlalchemy import Column, String, ForeignKey, Date
from app.database import Base
import datetime
from config import NodeType
from common.log import logging, LOG_LEVEL, log_handler
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)


class Server(Base):
    __tablename__ = 'server'
    hostname = Column(String, primary_key=True)
    type  = Column(String)
    login = Column(String)
    key_file = Column(String)
    created = Column(Date(), default=datetime.date.today())
    __mapper_args__ = {
        'polymorphic_identity':'server',
        'polymorphic_on':type
    }
    def __repr__(self):
        return ("hostname={0}, type={1}, login={2}, key_file{3}, created{4}".format(self.hostname, self.type, self.login, self.key_file, self.created))


class Peer(Server):
    __tablename__ = 'peer'
    id = Column(String, ForeignKey('server.hostname'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':NodeType.PEER,
    }

class Orderer(Server):
    __tablename__ = 'orderer'
    id = Column(String, ForeignKey('server.hostname'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':NodeType.ORDERER,
    }

class Ca(Server):
    __tablename__ = 'ca'
    id = Column(String, ForeignKey('server.hostname'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':NodeType.CA,
    }

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True)
    password = Column(String)
    email = Column(String)



