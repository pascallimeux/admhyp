# -*- coding: utf-8 -*-
'''
Created on 30 june 2017
@author: pascal limeux
'''

from sqlalchemy import Column, String, ForeignKey
from app.node.model import Node, check_deployed, check_started
from app.common.constants import NodeType, PEERPROCESSNAME
from app.common.log import get_logger
from app.common.lcmds import exec_local_cmd
from app.common.commands import build_folders, write_deployed, uncompress_files, start_peer, compress_locales_files_4_peer
logger = get_logger()

class Peer(Node):
    __tablename__ = 'peer'
    id = Column(String, ForeignKey('node.name'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':NodeType.PEER,
    }
    ca = Column(String, ForeignKey("ca.id"))

    def get_ca(self):
        return self.ca

    def get_type(self):
        return NodeType.PEER

    def get_process_name(self):
        return PEERPROCESSNAME

    def deploy(self):
        '''
        deploy PEER server
        '''
        logger.debug ("Deploy a peer:{}".format(self.hostname))
        if self.is_deployed():
            raise Exception ("PEER already deployed!")
        self.exec_command(build_folders(self.login), sudo=True)
        exec_local_cmd(compress_locales_files_4_peer())
        self.upload_file("/tmp/files.tgz", "/var/hyperledger/files.tgz")
        self.exec_command(uncompress_files())
        self.exec_command(write_deployed(self.get_type()))

    @check_deployed
    def start(self):
        logger.debug ("Start a peer:{}".format(self.hostname))
        if self.is_started():
            raise Exception ("PEER already started!")
        self.exec_command(start_peer(peer_name=self.hostname))

