# -*- coding: utf-8 -*-
'''
Created on 30 june 2017
@author: pascal limeux
'''

from app.common.services import Services, ObjectNotFoundException
from app.node.model import Node, NodeInfo
from app.database import get_session
from app.common.log import get_logger
import datetime, arrow
logger = get_logger()

class NodeServices(Services):

    def get_nodes(self):
        return Node.query.all()

    def get_node(self, name):
        node = Node.query.filter(Node.name == name).first()
        if node == None:
            raise ObjectNotFoundException("no node for name:{}".format(name))
        return node

    def update_info(self, sysinfo_dto):
        try:
            hostname = sysinfo_dto.agentId

            info = NodeInfo()
            info.totalmem = sysinfo_dto.total_memory
            info.freemem = sysinfo_dto.free_memory
            info.usedmem = sysinfo_dto.used_memory
            info.totaldisk = sysinfo_dto.total_disk
            info.freedisk = sysinfo_dto.free_disk
            info.useddisk = sysinfo_dto.used_disk
            info.cpusused = ''.join(sysinfo_dto.cpu_used)
            info.is_ca_deployed = sysinfo_dto.is_ca_deployed
            info.is_peer_deployed = sysinfo_dto.is_peer_deployed
            info.is_ca_started = sysinfo_dto.is_ca_started
            info.is_peer_started = sysinfo_dto.is_peer_started
            info.is_orderer_started = sysinfo_dto.is_orderer_started
            info.created = arrow.get(sysinfo_dto.created).datetime.replace(tzinfo=None) # convert to python datatime
            nodes = Node.query.filter(Node.hostname == hostname)
            for node in nodes:
                node.infos.append(info)

            get_session().commit()
        except Exception as e:
            get_session().rollback()
            logger.error(e)
            raise Exception("System info not updated, database error!")
        return node
