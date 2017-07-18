# -*- coding: utf-8 -*-
'''
Created on 29 june 2017
@author: pascal limeux
'''

from flask import flash, render_template, request
from flask import Blueprint
from app.peer.forms import PeerForm, MspForm
from app.peer.services import PeerServices
from app.ca.services import CaServices
from common.log import get_logger
logger = get_logger()
from app.login.views import login_required


peer_app = Blueprint('peer_app',__name__)

peerService = PeerServices()
caService = CaServices()

@peer_app.route("/peer", methods=['GET', 'POST'])
@login_required
def create():
    logger.debug("{0} /peer resource invocation".format(request.method))
    form = PeerForm(request.form)
    logger.error(form.errors)
    try:
        cas = caService.get_cas()
    except Exception as e:
        flash('Error: {}'.format(e))

    if request.method == 'POST':
        hostname=request.form['hostname']
        key_file=request.form['keyfile']
        pub_key_file=request.form['pubkeyfile']
        remoteadmlogin=request.form['radmlogin']
        remotelogin=request.form['rlogin']
        remotepassword=request.form['rpassword']
        try:
            logger.debug("hostname:{0} key_file:{1} pubkeyfile:{2} radmlogin:{3} rlogin:{4} rpassword:{5}".format(hostname, key_file, pub_key_file, remoteadmlogin, remotelogin, remotepassword))
            if not form.validate():
                flash('Error:{}'.format(form.errors))
            peerService.create_peer(hostname=hostname, remoteadmlogin=remoteadmlogin,  remotepassword=remotepassword, remotelogin=remotelogin, pub_key_file=pub_key_file, key_file=key_file)
            flash("new peer created: (hostname={0})".format(hostname))
        except Exception as e:
            flash('Error: {}'.format(e))
    return render_template('peer/peer.html', form=form, cas=cas)

@peer_app.route("/peers")
@login_required
def list():
    logger.debug("{0} /listpeers resource invocation".format(request.method))
    try:
        peers = peerService.get_peers()
    except Exception as e:
        flash('Error: {}'.format(e))
    return render_template('peer/peers.html', peers=peers)

@peer_app.route("/peer/<hostname>")
@login_required
def manage(hostname):
    logger.debug("{0} /peer/{1} resource invocation".format(request.method, hostname))
    try:
        cas = caService.get_cas()
        peer = peerService.get_peer(hostname)
    except Exception as e:
        flash('Error: {}'.format(e))
    return render_template('peer/peermngt.html', peer=peer, cas=cas)

@peer_app.route("/peer/<hostname>/deploy")
@login_required
def deploy(hostname):
    logger.debug("{0} /peer/{1}/deploy resource invocation".format(request.method, hostname))
    try:
        peers = peerService.deploy(hostname)
        logger.debug("peers:{}".format(peers))
        for peer in peers:
            logger.debug("peer: {}".format(peer.hostname))
    except Exception as e:
        flash('Error: {}'.format(e))
    return render_template('peer/peers.html', peers=peers)

@peer_app.route("/peer/<hostname>/start")
@login_required
def start(hostname):
    logger.debug("{0} /peer/{1}/start resource invocation".format(request.method, hostname))
    try:
        peers = peerService.start(hostname)
        logger.debug("peers:{}".format(peers))
        for peer in peers:
            logger.debug("peer: {}".format(peer.hostname))
    except Exception as e:
        flash('Error: {}'.format(e))
    return render_template('peer/peers.html', peers=peers)

@peer_app.route("/peer/<hostname>/stop")
@login_required
def stop(hostname):
    logger.debug("{0} /peer/{1}/stop resource invocation".format(request.method, hostname))
    try:
        peers = peerService.stop(hostname)
        logger.debug("peers:{}".format(peers))
        for peer in peers:
            logger.debug("peer: {}".format(peer.hostname))
    except Exception as e:
        flash('Error: {}'.format(e))
    return render_template('peer/peers.html', peers=peers)

@peer_app.route("/peer/<hostname>/setca", methods=['GET', 'POST'])
@login_required
def setca (hostname):
    logger.debug("{0} /peer/{1}/setca resource invocation".format(request.method, hostname))
    form = MspForm(request.form)
    logger.error(form.errors)
    try:
        cas = caService.get_cas()
        peer = peerService.get_peer(hostname)
        if request.method == 'POST':
            ca_hostname = request.form['ca_hostname']
            ca = caService.get_ca(ca_hostname)
            nodename="peer_" + hostname
            ca.register_node(nodename=nodename, password="pwd")
            ca.enroll_node(nodename=nodename, password="pwd")
            tgz = ca.get_msp(nodename=nodename, hostname=hostname)
            peer.set_msp(tgz, nodename)
            return render_template('peer/peermngt.html', form=form, peer=peer, cas=cas)
    except Exception as e:
        flash('Error: {}'.format(e))
    return render_template('peer/peermngt.html', peer=peer, cas=cas)
