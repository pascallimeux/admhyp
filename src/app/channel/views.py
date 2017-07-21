# -*- coding: utf-8 -*-
'''
Created on 29 june 2017
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

channel_app = Blueprint('channel_app',__name__)


caService = CaServices()
peerService = PeerServices()
ordererService = OrdererServices()
channelService = ChannelServices()

@channel_app.route("/channel", methods=['GET', 'POST'])
@login_required
def create():
    logger.debug("{0} /channel resource invocation".format(request.method))
    form = ChannelForm(request.form)
    try:
        cas = caService.get_cas()
        orderers = ordererService.get_orderers()
        peers = peerService.get_peers()
    except Exception as e:
        flash('Error: {}'.format(e))

    if request.method == 'POST':
        try:
            if not form.validate():
                raise Exception(form.errors)
            channelname = request.form['channelname']
            ca_ids = request.form.getlist('ca_ids')
            orderer_ids=request.form.getlist('orderer_ids')
            peer_ids=request.form.getlist('peer_ids')
            channelService.create_channel(name=channelname, ca_ids=ca_ids, orderer_ids=orderer_ids, peer_ids=peer_ids)
            flash("new channel created: (\nname={0}\nca={1}\norderer={2}\npeer={3})".format(channelname, ca_ids, orderer_ids, peer_ids))
            logger.debug("Create channel({})".format(channelname))
        except Exception as e:
            logger.error(e)
            flash('Error: {}'.format(e))

    return render_template('channel/channel.html', form=form, cas=cas, orderers=orderers, peers=peers)

@channel_app.route("/channels")
@login_required
def list():
    logger.debug("{0} /channels resource invocation".format(request.method))
    try:
        channels = channelService.get_channels()
    except Exception as e:
        flash('Error: {}'.format(e))
    return render_template('channel/channels.html', channels=channels)


@channel_app.route("/channel/<name>", methods=['GET', 'POST'])
@login_required
def manage(name):
    logger.debug("{0} /ca/{1} resource invocation".format(request.method, name))
    try:
        channel = channelService.get_channel(name)
    except Exception as e:
        flash('Error: {}'.format(e))
    return render_template('channel/channelmngt.html', channel=channel)
