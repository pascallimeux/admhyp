# -*- coding: utf-8 -*-
'''
Created on 6 july 2017
@author: pascal limeux
'''

from flask import flash, render_template, request
from flask import Blueprint
from app.orderer.forms import OrdererForm, MspForm
from app.ca.services import CaServices
from app.orderer.services import OrdererServices
from common.log import get_logger
logger = get_logger()
from app.login.views import login_required


orderer_app = Blueprint('orderer_app',__name__)

ordererService = OrdererServices()
caService = CaServices()

@orderer_app.route("/orderer", methods=['GET', 'POST'])
@login_required
def create():
    logger.debug("{0} /orderer resource invocation".format(request.method))
    form = OrdererForm(request.form)
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
            if not form.validate():
                flash('Error:{}'.format(form.errors))
            ordererService.create_orderer(hostname=hostname, remoteadmlogin=remoteadmlogin,  remotepassword=remotepassword, remotelogin=remotelogin, pub_key_file=pub_key_file, key_file=key_file)
            flash("new orderer created: (hostname={0})".format(hostname))
        except Exception as e:
            flash('Error: {}'.format(e))
    return render_template('orderer/orderer.html', form=form)

@orderer_app.route("/orderers")
@login_required
def list():
    logger.debug("{0} /listorderers resource invocation".format(request.method))
    try:
        orderers = ordererService.get_orderers()
    except Exception as e:
        flash('Error: {}'.format(e))
    return render_template('orderer/orderers.html', orderers=orderers)


@orderer_app.route("/orderer/<hostname>")
@login_required
def manage(hostname):
    logger.debug("{0} /orderer/{1} resource invocation".format(request.method, hostname))
    try:
        cas = caService.get_cas()
        orderer = ordererService.get_orderer(hostname)
    except Exception as e:
        flash('Error: {}'.format(e))
    return render_template('orderer/orderermngt.html', orderer=orderer, cas=cas)

@orderer_app.route("/orderer/<hostname>/deploy")
@login_required
def deploy(hostname):
    logger.debug("{0} /orderer/{1}/deploy resource invocation".format(request.method, hostname))
    try:
        cas = caService.get_cas()
        orderer = ordererService.get_orderer(hostname)
        orderer.deploy()
    except Exception as e:
        flash('Error: {}'.format(e))
    return render_template('orderer/orderermngt.html', orderer=orderer, cas=cas)


@orderer_app.route("/orderer/<hostname>/start")
@login_required
def start(hostname):
    logger.debug("{0} /orderer/{1}/start resource invocation".format(request.method, hostname))
    try:
        cas = caService.get_cas()
        orderer = ordererService.get_orderer(hostname)
        orderer.start()
    except Exception as e:
        flash('Error: {}'.format(e))
    return render_template('orderer/orderermngt.html', orderer=orderer, cas=cas)


@orderer_app.route("/orderer/<hostname>/stop")
@login_required
def stop(hostname):
    logger.debug("{0} /orderer/{1}/stop resource invocation".format(request.method, hostname))
    try:
        cas = caService.get_cas()
        orderer = ordererService.get_orderer(hostname)
        orderer.stop()
    except Exception as e:
        flash('Error: {}'.format(e))
    return render_template('orderer/orderermngt.html', orderer=orderer, cas=cas)


@orderer_app.route("/orderer/<hostname>/setca", methods=['GET', 'POST'])
@login_required
def setca (hostname):
    logger.debug("{0} /orderer/{1}/setca resource invocation".format(request.method, hostname))
    form = MspForm(request.form)
    logger.error(form.errors)
    try:
        cas = caService.get_cas()
        orderer = ordererService.get_orderer(hostname)
        if request.method == 'POST':
            ca_hostname = request.form['ca_hostname']
            ca = caService.get_ca(ca_hostname)
            nodename="orderer_" + hostname
            ca.register_node(nodename=nodename, password="pwd")
            ca.enroll_node(nodename=nodename, password="pwd")
            tgz = ca.get_msp(nodename=nodename, hostname=hostname)
            orderer.set_msp(tgz, nodename)
            ordererService.add_ca(hostname, ca.id)
            return render_template('orderer/orderermngt.html', form=form, orderer=orderer, cas=cas)
    except Exception as e:
        flash('Error: {}'.format(e))
    return render_template('orderer/orderermngt.html', orderer=orderer, cas=cas)
