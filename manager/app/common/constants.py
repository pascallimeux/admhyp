# -*- coding: utf-8 -*-
'''
Created on 30 june 2017
@author: pascal limeux
'''

# nodes types
class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

NodeType = Enum(['PEER', 'CA', 'ORDERER', 'CHANNEL', 'ROOT'])
NodeStatus = Enum(['CREATED', 'NOTCONNECT', 'CONNECTED', 'UNDEPLOYED', 'DEPLOYED', 'STARTED', 'STOPPED'])

PEERPROCESSNAME="peer"
CASERVERPROCESSNAME="fabric-ca-server"
ORDERERPROCESSNAME="orderer"