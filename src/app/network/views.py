# -*- coding: utf-8 -*-
'''
Created on 8 august 2017
@author: pascal limeux
'''

from flask import flash, render_template, request
from flask import Blueprint
from app.channel.forms import ChannelForm
from app.orderer.services import OrdererServices
from app.peer.services import PeerServices
from app.channel.services import ChannelServices
from app.ca.services import CaServices
from app.common.log import get_logger
logger = get_logger()
from app.login.views import login_required
from app.common.constants import NodeType, NodeStatus
from app.network.services import NetworkServices
network_app = Blueprint('network_app',__name__)

netService = NetworkServices()

@network_app.route("/networks")
@login_required
def list():
    logger.debug("{0} /networks resource invocation".format(request.method))
    try:
        network = netService.create_network()
        return render_template('network/network.html', network=network, NodeType=NodeType, NodeStatus=NodeStatus)
    except Exception as e:
        flash('Error: {}'.format(e))
