# -*- coding: utf-8 -*-
'''
Created on 30 june 2017
@author: pascal limeux
'''

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base
from app.common.constants import NodeStatus
from app.common.rcmds import check_ssh_admin_connection
import datetime
from functools import wraps
from app.common.ssh import Ssh
from app.common.log import get_logger
import abc
from app.common.commands import is_started, is_deployed, stop_process, uncompress_msp, remote_file_4_upload_msp


logger = get_logger()


def check_deployed(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not  args[0].is_deployed():
            raise Exception("{} not deployed!".format(args[0].get_type()))
        return f(*args, **kwargs)
    return wrapper


def check_started(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not args[0].is_started():
            raise Exception("{} not started!".format(args[0].get_type()))
        return f(*args, **kwargs)
    return wrapper


class Node(Base):
    __tablename__ = 'node'
    name  = Column(String, primary_key=True)
    type  = Column(String)
    hostname = Column(String)
    login = Column(String)
    key_file = Column(String)
    is_deployed = Column(Boolean, default=False)
    created = Column(DateTime(), default=datetime.datetime.utcnow)
    info = relationship('NodeInfo', uselist=False, back_populates="node")
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
        err = ssh = None
        try:
            ssh = Ssh(hostname=self.hostname, username=self.login, key_file=self.key_file)
            out, err = ssh.exec_cmd(command, sudo=sudo)
        finally:
            if ssh:
                ssh.close_connection()
        if checkerr and err != "":
            raise Exception (err)
        return out, err

    def upload_file(self, localFile, remoteFile):
        ssh = None
        try:
            ssh = Ssh(hostname=self.hostname, username=self.login, key_file=self.key_file)
            ssh.upload_file(localFile, remoteFile)
        except Exception as e:
            logger.error(e)
            raise e
        finally:
            if ssh:
                ssh.close_connection()

    def download_file(self, remoteFile, localFile):
        ssh = None
        try:
            ssh = Ssh(hostname=self.hostname, username=self.login, key_file=self.key_file)
            ssh.download_file(remoteFile, localFile)
        except Exception as e:
            logger.error(e)
            raise e
        finally:
            if ssh:
                ssh.close_connection()

    def set_msp(self, tgz, nodename):
        logger.debug("set_msp on {0}({1})".format(self.get_type(), self.id))
        self.upload_file(tgz, remote_file_4_upload_msp())
        self.exec_command(uncompress_msp())

    def is_deployed(self):
        logger.debug ("Check if the {0}({1}) is deployed".format(self.get_type(), self.hostname))
        out, err = self.exec_command(is_deployed(self.get_type()))
        if "True" in out:
            return True
        return False

    def is_started(self):
        logger.debug ("Check if the {0}({1}) is started".format(self.get_process_name(), self.hostname))
        out, err = self.exec_command(is_started(self.get_process_name()))
        if "True" in out:
            return True
        return False

    @check_started
    def stop(self):
        logger.debug("Stop a {0}({1})".format(self.get_type(), self.hostname))
        self.exec_command(stop_process(self.get_process_name()))

    @abc.abstractmethod
    def get_type(self):
        return

    @abc.abstractmethod
    def get_process_name(self):
        return

    @abc.abstractmethod
    def deploy(self):
        return

    @abc.abstractmethod
    def start(self):
        return


class NodeInfo(Base):
    __tablename__ = 'node_info'
    name = Column(String, primary_key=True)
    totalmem = Column(Float)
    freemem = Column(Float)
    usedmem = Column(Float)
    totaldisk = Column(Float)
    freedisk = Column(Float)
    useddisk = Column(Float)
    cpusused = Column(String)
    is_ca_deployed = Column(Boolean, default=False)
    is_peer_deployed = Column(Boolean, default=False)
    is_orderer_deployed = Column(Boolean, default=False)
    is_ca_started = Column(Boolean, default=False)
    is_peer_started = Column(Boolean, default=False)
    is_orderer_started = Column(Boolean, default=False)
    created = Column(DateTime(), default=datetime.datetime.utcnow)
    node_name = Column(String, ForeignKey('node.name'))
    node = relationship("Node", back_populates="info")