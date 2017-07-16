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
from common.ssh import Ssh
from common.log import get_logger
import abc


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
        '''Get status of the node: CREATED, NOTCONNECT, CONNECTED, DEPLOYED, UNDEPLOYED, STARTED, STOPPED  '''
        self.status = NodeStatus.CREATED
        self.connect()
        if self.status == NodeStatus.CONNECTED:
            if self.is_deployed():
                self.status =  NodeStatus.DEPLOYED
                if self.is_started():
                    self.status = NodeStatus.STARTED
                else:
                    self.status = NodeStatus.STOPPED
            else:
                self.status =  NodeStatus.UNDEPLOYED
        else:
            self.status = NodeStatus.NOTCONNECT

        logger.info("Node:{0} Type:{1} Status:{2}".format(self.hostname, self.get_type(), self.status))
        return self.status

    def connect(self):
        if check_ssh_admin_connection(hostname=self.hostname, remoteadminlogin=self.login, key_file=self.key_file):
            self.status =  NodeStatus.CONNECTED

    def exec_command(self, command, sudo=False, checkerr=True):
        err = None
        try:
            ssh = Ssh(hostname=self.hostname, username=self.login, key_file=self.key_file)
            out, err = ssh.exec_cmd(command, sudo=sudo)
        except Exception as e:
            logger.error(e)
            return err
        finally:
            ssh.close_connection()
        if checkerr and err != "":
            raise Exception (err)
        return out, err

    def upload_file(self, localFile, remoteFile):
        try:
            ssh = Ssh(hostname=self.hostname, username=self.login, key_file=self.key_file)
            ssh.upload_file(localFile, remoteFile)
        except Exception as e:
            logger.error(e)
            raise e
        finally:
            ssh.CloseConnection()

    @abc.abstractmethod
    def is_deployed(self):
        return False

    @abc.abstractmethod
    def is_started(self):
        return False

    @abc.abstractmethod
    def deploy(self):
        return

    @abc.abstractmethod
    def start(self):
        return

    @abc.abstractmethod
    def stop(self):
        return

    @abc.abstractmethod
    def get_type(self):
        return
