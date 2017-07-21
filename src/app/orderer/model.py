# -*- coding: utf-8 -*-
'''
Created on 7 july 2017
@author: pascal limeux
'''

from sqlalchemy import Column, String, ForeignKey
from app.node.model import Node, check_deployed
from app.common.constants import NodeType, ORDERERPROCESSNAME
from app.common.log import get_logger
logger = get_logger()
from app.common.log import get_logger
from app.common.lcmds import exec_local_cmd
from app.common.commands import build_folders, write_deployed, uncompress_files, start_orderer, compress_locales_files_4_orderer
logger = get_logger()



class Orderer(Node):
    __tablename__ = 'orderer'
    id = Column(String, ForeignKey('node.name'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':NodeType.ORDERER,
    }
    ca = Column(String, ForeignKey("ca.id"))

    def get_ca(self):
        return self.ca

    def get_type(self):
        return NodeType.ORDERER

    def get_process_name(self):
        return ORDERERPROCESSNAME

    def deploy(self):
        '''
        deploy ORDERER server
        '''
        logger.debug ("Deploy orderer:{}".format(self.name))
        if self.is_deployed():
            raise Exception ("ORDERER already deployed!")
        self.exec_command(build_folders(self.login), sudo=True)
        exec_local_cmd(compress_locales_files_4_orderer())
        self.upload_file("/tmp/files.tgz", "/var/hyperledger/files.tgz")
        self.exec_command(uncompress_files())
        self.exec_command(write_deployed(self.get_type()))

    @check_deployed
    def start(self):
        logger.debug ("Start orderer:{}".format(self.name))
        if self.is_started():
            raise Exception ("ORDERER already started!")
        self.exec_command(start_orderer())
