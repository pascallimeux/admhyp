# -*- coding: utf-8 -*-
'''
Created on 30 june 2017
@author: pascal limeux
'''

from sqlalchemy import Column, String, ForeignKey
import time
from app.node.model import Node
from app.common.constants import NodeType, CASERVERPROCESSNAME
from common.log import get_logger
from core.localcommands import exec_local_cmd
from common.commands import start_ca, build_folders, compress_locales_files_4_ca, uncompress_files, register_admin, enroll_admin, is_started, is_deployed, stop_process, write_deployed, enroll_user, enroll_node, register_node, register_user, compress_msp, remote_file_4_download_msp
logger = get_logger()




class Ca(Node):
    __tablename__ = 'ca'
    id = Column(String, ForeignKey('node.name'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':NodeType.CA,
    }

    def get_process_name(self):
        return CASERVERPROCESSNAME

    def get_type(self):
        return NodeType.CA


    def deploy(self):
        '''
        deploy CA server and enroll the default admin, cf config file
        '''
        logger.debug ("Deploy a ca:{}".format(self.hostname))
        if self.is_deployed():
            raise Exception ("CA already deployed!")
        self.exec_command(build_folders(self.login), sudo=True)
        exec_local_cmd(compress_locales_files_4_ca())
        self.upload_file("/tmp/files.tgz", "/var/hyperledger/files.tgz")
        self.exec_command(uncompress_files())
        self.exec_command(start_ca())
        self.exec_command(enroll_admin(self.login),checkerr=False) # enroll default admin
        self.exec_command(stop_process(self.get_process_name()))
        self.exec_command(write_deployed(self.get_type()))

    def start(self):
        logger.debug ("Start a ca:{}".format(self.hostname))
        self.check_deployed()
        if self.is_started():
            raise Exception ("CA already started!")
        self.exec_command(start_ca())

    def create_admin(self, username, password):
        self.check_started()
        self.exec_command(register_admin(username, password))
        self.exec_command(enroll_admin(username, password))

    def register_user(self, username, password):
        logger.debug("Register user:{}".format(username))
        self.check_started()
        self.exec_command(register_user(username, password), checkerr=False)
        logger.debug ("{} is now register".format(username))

    def register_node(self, nodename, password):
        logger.debug("Register node:{}".format(nodename))
        self.check_started()
        self.exec_command(register_node(nodename, password), checkerr=False)
        logger.debug("{} is now register".format(nodename))

    def enroll_user(self, username, password):
        logger.debug("Enroll user:{}".format(username))
        self.check_started()
        self.exec_command(enroll_user(username, password), checkerr=False)
        logger.debug("{} is now enroll".format(username))

    def enroll_node(self, nodename, password):
        logger.debug("Enroll node:{}".format(nodename))
        self.check_started()
        self.exec_command(enroll_node(nodename, password), checkerr=False)
        logger.debug("{} is now enroll".format(nodename))

    def get_msp(self, nodename, name):
        logger.debug("copy_msp on:{}".format(name))
        self.check_started()
        tgz = "/tmp/{0}.tgz".format(nodename)
        self.exec_command(compress_msp(nodename))
        self.download_file(remoteFile=remote_file_4_download_msp(nodename=nodename), localFile=tgz)
        return tgz
