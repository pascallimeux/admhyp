# -*- coding: utf-8 -*-
'''
Created on 30 june 2017
@author: pascal limeux
'''

from app.common.services import Services, ObjectNotFoundException
from app.node.model import Node, NodeInfo
from app.database import get_session
from app.common.log import get_logger
logger = get_logger()

class NodeServices(Services):

    def get_nodes(self):
        return Node.query.all()

    def get_node(self, name):
        node = Node.query.filter(Node.name == name).first()
        if node == None:
            raise ObjectNotFoundException("no node for name:{}".format(name))
        return node

    def update_info(self, message):
        try:
            nodename = message.AgentId
            #info.created = message.Created
            info = NodeInfo()
            info.name = nodename
            info.totalmem = message.total_memory
            info.freemem = message.free_memory
            info.usedmem = message.used_memory
            info.totaldisk = message.total_disk
            info.freedisk = message.free_disk
            info.useddisk = message.used_disk
            info.cpusused = ''.join(message.cpu_used)
            info.is_ca_deployed = message.is_ca_deployed
            info.is_peer_deployed = message.is_peer_deployed
            info.is_ca_started = message.is_ca_started
            info.is_peer_started = message.is_peer_started
            info.is_orderer_started = message.is_orderer_started
            if NodeInfo.query.filter(NodeInfo.name == nodename).first() != None:
                old_info = get_session().query(NodeInfo).filter(NodeInfo.name == nodename)
                old_info.delete()
            node = self.get_node(nodename)
            node.info=info
            get_session().commit()
        except Exception as e:
            get_session().rollback()
            raise Exception("System info not updated, database error!")
        return node
