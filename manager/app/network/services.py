# -*- coding: utf-8 -*-
'''
Created on 9 august 2017
@author: pascal limeux
'''
from app.common.services import Services
from app.channel.services import ChannelServices
from app.common.log import get_logger
from app.node.model import Node
import json
from app.common.constants import NodeType, NodeStatus
logger = get_logger()
channelService = ChannelServices()


class D3RootNode():
    def __init__(self, nodes):
        self.nodes = nodes

    def to_json(self):
        js = json.dumps(self, default=lambda o: o.__dict__)
        return js


class D3Node():
    def __init__(self, name, type, hostname="", size=0, children=[], state=NodeStatus.CREATED):
        self.name = name
        if size != 0:
            self.size = size
        if len(children) != 0:
            self.children = children
        self.hostname = hostname
        self.state = state
        self.type = type



def build_mock_network():
    peer1 = D3Node(name="peer1", type = NodeType.PEER, state = NodeStatus.STARTED)
    peer2 = D3Node(name="peer2", type = NodeType.PEER, state = NodeStatus.STARTED)
    peer3 = D3Node(name="peer3", type = NodeType.PEER, state = NodeStatus.STARTED)
    ca1 = D3Node(name="ca1", type = NodeType.CA, state=NodeStatus.UNDEPLOYED)
    ca2 = D3Node(name="ca2", type = NodeType.CA, state=NodeStatus.STARTED)
    orderer1 = D3Node(name="orderer1", type = NodeType.ORDERER, state = NodeStatus.CONNECTED)
    orderer2 = D3Node(name="orderer2", type = NodeType.ORDERER, state = NodeStatus.STARTED)
    orderer3 = D3Node(name="orderer3", type = NodeType.ORDERER, state = NodeStatus.STOPPED)
    orderer4 = D3Node(name="orderer4", type = NodeType.ORDERER, state = NodeStatus.DEPLOYED)
    channel1 = D3Node(name="channel1", type = NodeType.CHANNEL, children=[ca1, peer1, peer2, peer3, orderer1, orderer2], state = NodeStatus.STOPPED)
    channel2 = D3Node(name="channel2", type = NodeType.CHANNEL, children=[ca2, peer1, orderer1, orderer2, orderer3, orderer4])
    channel3 = D3Node(name="channel3", type = NodeType.CHANNEL, children=[peer1, peer2, orderer1])
    nodes = D3Node(name="RootNode", children=[channel1, channel2, channel3], type = NodeType.ROOT)
    rootnode = D3RootNode(nodes=nodes)
    return rootnode.to_json()

def create_D3node(node):
    return D3Node(name=node.name, type=node.type, hostname=node.hostname, state=node.get_status())

class NetworkServices(Services):

    def create_network(self):
        try:
            channels = channelService.get_channels()
            D3channels = []
            for channel in channels:
                children = []
                for peer in channel.peers:
                    children.append(create_D3node(peer))

                for orderer in channel.orderers:
                    children.append(create_D3node(orderer))

                for ca in channel.cas:
                    children.append(create_D3node(ca))

                D3channels.append(D3Node(name=channel.name, type=NodeType.CHANNEL, children=children))
            nodes = D3Node(name="RootNode", children=D3channels, type=NodeType.ROOT)
            rootnode = D3RootNode(nodes=nodes)
            logger.debug("network:{}".format(rootnode))
            network = rootnode.to_json()
            #network = build_mock_network()
        except Exception as e:
            logger.error("{0}".format(e))
            raise Exception("network creation failled!")
        return network

