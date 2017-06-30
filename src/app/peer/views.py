# -*- coding: utf-8 -*-
'''
Created on 29 june 2017
@author: pascal limeux
'''

from common.log import logging, LOG_LEVEL, log_handler
from app.common.views import Check_authorized_access
from flask import Flask, flash, redirect, render_template, request, session, abort
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask import Blueprint
from rcmd import CreateRemoteAdmin
from nodeManager import NodeManager
from app.peer.forms import PeerForm
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)

peer_app = Blueprint('peer_app',__name__)

@peer_app.route("/peer", methods=['GET', 'POST'])
def peer():
    logger.debug("{0} /peer resource invocation".format(request.method))
    form = PeerForm(request.form)
    logger.error(form.errors)
    if request.method == 'POST':
        hostname=request.form['hostname']
        key_file=request.form['keyfile']
        pub_key_file=request.form['pubkeyfile']
        remoteadmlogin=request.form['radmlogin']
        remotelogin=request.form['rlogin']
        remotepassword=request.form['rpassword']
        try:
            logger.debug("hostname:{0} key_file:{1} pubkeyfile:{2} radmlogin:{3} rlogin:{4} rpassword:{5}".format(hostname, key_file, pub_key_file, remoteadmlogin, remotelogin, remotepassword))
            CreateRemoteAdmin(hostname=hostname, password=remotepassword, username=remotelogin, pub_key_file=pub_key_file)
            nodeManager = NodeManager()
            nodeManager.CreatePeer(hostname=hostname, remoteAdmin=remoteadmlogin, key_file=key_file)
        except Exception as e:
            flash('Error: {}'.format(e))

        if form.validate():
            # Save the comment here.
            flash(hostname + ' is now installed')
        else:
            flash('Error: All the form fields are required. ')
    if session.get('logged_in'):
        return render_template('peer.html', form=form)
    else:
        logger.info("Unauthorized access from ip:{}".format(request.remote_addr))
        return render_template('401.html')
