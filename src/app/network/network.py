# -*- coding: utf-8 -*-
'''
Created on 7 august 2017
@author: pascal limeux
'''
import json
import html
from app.common.constants import NodeType, NodeStatus


class RootNode():
    def __init__(self, nodes):
        self.nodes = nodes

    def to_json(self):
        js = json.dumps(self, default=lambda o: o.__dict__)
        return html.unescape(js)


class Node():
    def __init__(self, name, type, size=0, children=[], state=NodeStatus.CREATED):
        self.name = name
        if size != 0:
            self.size = size
        if len(children) != 0:
            self.children = children
        self.state = state
        self.type = type



def build_mock_network():
    peer1 = Node(name="peer1", type = NodeType.PEER, state = NodeStatus.STARTED)
    peer2 = Node(name="peer2", type = NodeType.PEER, state = NodeStatus.STARTED)
    peer3 = Node(name="peer3", type = NodeType.PEER, state = NodeStatus.STARTED)
    ca1 = Node(name="ca1", type = NodeType.CA, state=NodeStatus.UNDEPLOYED)
    ca2 = Node(name="ca2", type = NodeType.CA, state=NodeStatus.STARTED)
    orderer1 = Node(name="orderer1", type = NodeType.ORDERER, state = NodeStatus.CONNECTED)
    orderer2 = Node(name="orderer2", type = NodeType.ORDERER, state = NodeStatus.STARTED)
    orderer3 = Node(name="orderer3", type = NodeType.ORDERER, state = NodeStatus.STOPPED)
    orderer4 = Node(name="orderer4", type = NodeType.ORDERER, state = NodeStatus.DEPLOYED)
    channel1 = Node(name="channel1", type = NodeType.CHANNEL, children=[ca1, peer1, peer2, peer3, orderer1, orderer2], state = NodeStatus.STOPPED)
    channel2 = Node(name="channel2", type = NodeType.CHANNEL, children=[ca2, peer1, orderer1, orderer2, orderer3, orderer4])
    channel3 = Node(name="channel3", type = NodeType.CHANNEL, children=[peer1, peer2, orderer1])
    nodes = Node(name="RootNode", children=[channel1, channel2, channel3], type = NodeType.ROOT)
    rootnode = RootNode(nodes=nodes)
    return rootnode.to_json()

if __name__== '__main__':
    nodes = build_mock_network()
    print (nodes)