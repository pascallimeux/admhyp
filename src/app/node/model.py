# -*- coding: utf-8 -*-
'''
Created on 30 june 2017
@author: pascal limeux
'''

from sqlalchemy import Column, String, ForeignKey, Date, Boolean
from app.database import Base
from app.common.constants import NodeStatus
from core.remotecommands import check_ssh_admin_connection
import datetime
from common.log import get_logger
logger = get_logger()


class Node(Base):
    __tablename__ = 'node'
    hostname = Column(String, primary_key=True)
    type  = Column(String)
    login = Column(String)
    key_file = Column(String)
    is_deployed = Column(Boolean, default=False)
    created = Column(Date(), default=datetime.date.today())
    __mapper_args__ = {
        'polymorphic_identity':'server',
        'polymorphic_on':type
    }

    def __repr__(self):
        return ("hostname={0}, type={1}, login={2}, key_file{3}, created{4}".format(self.hostname, self.type, self.login, self.key_file, self.created))

    def get_status(self):
        self.status =  NodeStatus.CREATED
        if check_ssh_admin_connection(hostname=self.hostname, remoteadminlogin=self.login, key_file=self.key_file):
            self.status =  NodeStatus.CONNECTED
            if self.check_deployed():
                self.status =  NodeStatus.DEPLOYED
                if self.check_started():
                    self.Status = NodeStatus.STARTED
                else:
                    self.Status = NodeStatus.STOPPED
        return self.status

    def check_ssh_admin_cnx(self):
        if check_ssh_admin_connection(hostname=self.hostname, remoteadminlogin=self.login, key_file=self.key_file):
            self.status =  NodeStatus.CONNECTED
        else:
            self.status =  NodeStatus.NOTCONNECTED

    def check_deployed(self):
        return False

    def check_started(self):
        return False