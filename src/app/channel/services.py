# -*- coding: utf-8 -*-
'''
Created on 20 july 2017
@author: pascal limeux
'''
from app.common.services import Services, ObjectNotFoundException
from app.channel.model import Channel
from app.database import get_session
from app.ca.services import CaServices
from app.orderer.services import OrdererServices
from app.peer.services import PeerServices
from app.common.log import get_logger
logger = get_logger()
caService = CaServices()
peerService = PeerServices()
ordererService = OrdererServices()
class ChannelServices(Services):

    def create_channel(self, name, ca_ids, orderer_ids, peer_ids):
        try:
            cas = []
            orderers = []
            peers = []
            for ca_id in ca_ids:
                cas.append(caService.get_ca(ca_id))
            for ord_id in orderer_ids:
                orderers.append(ordererService.get_orderer(ord_id))
            for pe_id in peer_ids:
                peers.append(peerService.get_peer(pe_id))
            channel = Channel(name=name, cas=cas, orderers=orderers, peers=peers)
            self.SaveRecord(channel)
        except Exception as e:
            get_session().rollback()
            logger.error("{0}".format(e))
            raise Exception("Data not record, database error!")
        return channel

    def remove_channel(self, name):
        objs = self.get_session().query(Channel).filter(Channel.name == name)
        ret = objs.delete()
        get_session().commit()
        return ret

    def get_channel(self, name):
        channel = Channel.query.filter(Channel.name == name).first()
        if channel == None:
            raise ObjectNotFoundException()
        logger.debug(channel)
        return channel

    def get_channels(self):
        return Channel.query.all()