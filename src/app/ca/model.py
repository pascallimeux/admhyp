# -*- coding: utf-8 -*-
'''
Created on 30 june 2017
@author: pascal limeux
'''

from sqlalchemy import Column, String, ForeignKey
import time
from app.node.model import Node
from app.common.constants import NodeType, NodeStatus
from common.log import get_logger
from core.localcommands import exec_local_cmd
from common.commands import start_ca, build_folders, compress_locales_files_4_ca, uncompress_ca_files, register_admin, enroll_admin, is_ca_started, is_ca_deployed, stop_ca, write_ca_deployed, enroll_user, enroll_node, register_node, register_user, compress_msp
logger = get_logger()

class Ca(Node):
    __tablename__ = 'ca'
    id = Column(String, ForeignKey('node.hostname'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':NodeType.CA,
    }

    def get_type(self):
        return NodeType.CA

    def deploy(self):
        '''
        deploy CA server and enroll the default admin, cf config file
        '''
        logger.debug ("Deploy a ca:{}".format(self.hostname))
        if self.is_deployed():
            raise Exception ("CA already deployeds!")
        self.exec_command(build_folders(self.login), sudo=True)
        exec_local_cmd(compress_locales_files_4_ca())
        self.upload_file("/tmp/files.tgz", "/var/hyperledger/files.tgz")
        self.exec_command(uncompress_ca_files())
        self.exec_command(start_ca())
        self.exec_command(enroll_admin(self.login),checkerr=False) # enroll default admin
        self.exec_command(stop_ca())
        self.exec_command(write_ca_deployed())

    def start(self):
        logger.debug ("Start a ca:{}".format(self.hostname))
        if self.is_started():
            raise Exception ("CA already started!")
        if not self.is_deployed():
            raise Exception ("CA is not deployed")
        self.exec_command(start_ca())


    def stop(self):
        logger.debug ("Stop a ca:{}".format(self.hostname))
        if not self.is_deployed():
            raise Exception ("CA not deployed!")
        if not self.is_started():
            raise Exception ("CA already stopped!")
        self.exec_command(stop_ca())


    def is_deployed(self):
        logger.debug ("Check if the ca:{} is deployed".format(self.hostname))
        out, err = self.exec_command(is_ca_deployed())
        if "True" in out:
            return True
        return False

    def is_started(self):
        logger.debug ("Check if the ca:{} is started".format(self.hostname))
        out, err = self.exec_command(is_ca_started())
        if "True" in out:
            return True
        return False

    def create_admin(self, username, password):
        self.exec_command(register_admin(username, password))
        self.exec_command(enroll_admin(username, password))

    def register_user(self, username, password):
        logger.debug("Register user:{}".format(username))
        if not self.is_started():
            raise Exception ("CA not running!")
        self.exec_command(register_user(username, password), checkerr=False)
        logger.debug ("{} is now register".format(username))

    def register_node(self, nodename, password):
        logger.debug("Register node:{}".format(nodename))
        if not self.is_started():
            raise Exception ("CA not running!")
        self.exec_command(register_node(nodename, password), checkerr=False)
        logger.debug("{} is now register".format(nodename))

    def enroll_user(self, username, password):
        logger.debug("Enroll user:{}".format(username))
        if not self.is_started():
            raise Exception ("CA not running!")
        self.exec_command(enroll_user(username, password), checkerr=False)
        logger.debug("{} is now enroll".format(username))

    def enroll_node(self, nodename, password):
        logger.debug("Enroll node:{}".format(nodename))
        if not self.is_started():
            raise Exception ("CA not running!")
        self.exec_command(enroll_node(nodename, password), checkerr=False)
        logger.debug("{} is now enroll".format(nodename))

    def get_msp(self, nodename, hostname):
        logger.debug("copy_msp on:{}".format(hostname))
        if not self.is_started():
            raise Exception ("CA not running!")
        tgz = "/tmp/{0}.tgz".format(nodename)
        self.exec_command(compress_msp(nodename))
        self.download_file( remoteFile="/var/hyperledger/.msp/{0}/{0}.tgz".format(nodename), localFile=tgz)
        return tgz
