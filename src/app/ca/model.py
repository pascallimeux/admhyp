# -*- coding: utf-8 -*-
'''
Created on 30 june 2017
@author: pascal limeux
'''

from sqlalchemy import Column, String, ForeignKey
from app.node.model import Node, check_deployed, check_started
from app.common.constants import NodeType, CASERVERPROCESSNAME
from app.common.log import get_logger
from app.common.lcmds import exec_local_cmd
from app.common.commands import start_ca, build_folders, compress_locales_files_4_ca, uncompress_files, register_admin, enroll_admin, stop_process, write_deployed, enroll_user, enroll_node, register_node, register_user, compress_msp, remote_file_4_download_msp
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

    @check_deployed
    def start(self):
        logger.debug ("Start a ca:{}".format(self.hostname))
        if self.is_started():
            raise Exception ("CA already started!")
        self.exec_command(start_ca())

    @check_started
    def create_admin(self, username, password):
        self.exec_command(register_admin(username, password))
        self.exec_command(enroll_admin(username, password))

    @check_started
    def register_user(self, username, password):
        logger.debug("Register user:{}".format(username))
        self.exec_command(register_user(username, password), checkerr=False)
        logger.debug ("{} is now register".format(username))

    @check_started
    def register_node(self, nodename, password):
        logger.debug("Register node:{}".format(nodename))
        self.exec_command(register_node(nodename, password), checkerr=False)
        logger.debug("{} is now register".format(nodename))

    @check_started
    def enroll_user(self, username, password):
        logger.debug("Enroll user:{}".format(username))
        self.check_started()
        self.exec_command(enroll_user(username, password), checkerr=False)
        logger.debug("{} is now enroll".format(username))

    @check_started
    def enroll_node(self, nodename, password):
        logger.debug("Enroll node:{}".format(nodename))
        self.exec_command(enroll_node(nodename, password), checkerr=False)
        logger.debug("{} is now enroll".format(nodename))

    @check_started
    def get_msp(self, name):
        logger.debug("copy_msp on:{}".format(name))
        tgz = "/tmp/{0}.tgz".format(name)
        self.exec_command(compress_msp(name))
        self.download_file(remoteFile=remote_file_4_download_msp(nodename=name), localFile=tgz)
        return tgz
