# -*- coding: utf-8 -*-
'''
Created on 6 july 2017
@author: pascal limeux
'''


from flask import flash, request, Blueprint, render_template
from app.ca.forms import CaForm, RegisterForm
from app.login.views import login_required
from app.ca.services import CaServices
from common.log import get_logger
logger = get_logger()
ca_app = Blueprint('ca_app',__name__)

caService = CaServices()


@ca_app.route("/ca", methods=['GET', 'POST'])
@login_required
def create():
    logger.debug("{0} /ca resource invocation".format(request.method))
    form = CaForm(request.form)
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
            caService.create_ca(hostname=hostname, remoteadmlogin=remoteadmlogin,  remotepassword=remotepassword, remotelogin=remotelogin, pub_key_file=pub_key_file, key_file=key_file)
            flash("new ca created: (hostname={0})".format(hostname))
        except Exception as e:
            flash('Error: {}'.format(e))
    return render_template('ca/ca.html', form=form)

@ca_app.route("/cas")
@login_required
def list():
    logger.debug("{0} /listcas resource invocation".format(request.method))
    try:
        cas = caService.get_cas()
    except Exception as e:
        flash('Error: {}'.format(e))
    return render_template('ca/cas.html', cas=cas)

@ca_app.route("/ca/<hostname>", methods=['GET', 'POST'])
@login_required
def manage(hostname):
    logger.debug("{0} /ca/{1} resource invocation".format(request.method, hostname))
    form = RegisterForm(request.form)
    logger.error(form.errors)
    try:
        ca = caService.get_ca(hostname)
    except Exception as e:
        flash('Error: {}'.format(e))
    return render_template('ca/camngt.html', ca=ca)

@ca_app.route("/ca/<hostname>/deploy")
@login_required
def deploy(hostname):
    logger.debug("{0} /ca/{1}/deploy resource invocation".format(request.method, hostname))
    try:
        ca = caService.get_ca(hostname)
        ca.deploy()
    except Exception as e:
        flash('Error: {}'.format(e))
    return render_template('ca/camngt.html', ca=ca)

@ca_app.route("/ca/<hostname>/start")
@login_required
def start(hostname):
    logger.debug("{0} /ca/{1}/start resource invocation".format(request.method, hostname))
    try:
        ca = caService.get_ca(hostname)
        ca.start()
    except Exception as e:
        flash('Error: {}'.format(e))
    return render_template('ca/camngt.html', ca=ca)

@ca_app.route("/ca/<hostname>/stop")
@login_required
def stop(hostname):
    logger.debug("{0} /ca/{1}/stop resource invocation".format(request.method, hostname))
    try:
        ca = caService.get_ca(hostname)
        ca.stop()
    except Exception as e:
        flash('Error: {}'.format(e))
    return render_template('ca/camngt.html', ca=ca)

@ca_app.route("/ca/<hostname>/register", methods=['GET', 'POST'])
@login_required
def register(hostname):
    logger.debug("{0} /ca/{1}/register resource invocation".format(request.method, hostname))
    form = RegisterForm(request.form)
    logger.error(form.errors)
    try:
        ca = caService.get_ca(hostname)
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if not form.validate():
                flash('Error:{}'.format(form.errors))
            ca.register_user(username=username, password=password)
            flash("new user register: {0}".format(username))
            return render_template('ca/camngt.html', form=form, ca=ca)
    except Exception as e:
        flash('Error: {}'.format(e))
    return render_template('ca/camngt.html', ca=ca)

@ca_app.route("/ca/<hostname>/createadmin", methods=['GET', 'POST'])
@login_required
def create_admin(hostname):
    logger.debug("{0} /ca/{1}/createadmin resource invocation".format(request.method, hostname))
    form = RegisterForm(request.form)
    logger.error(form.errors)
    try:
        ca = caService.get_ca(hostname)
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if not form.validate():
                flash('Error:{}'.format(form.errors))
            ca.create_admin(username=username, password=password)
            flash("admin created: {0}".format(username))
            return render_template('ca/camngt.html', form=form, ca=ca)
    except Exception as e:
        flash('Error: {}'.format(e))
    return render_template('ca/camngt.html', ca=ca)

@ca_app.route("/ca/<hostname>/enroll", methods=['GET', 'POST'])
@login_required
def enroll(hostname):
    logger.debug("{0} /ca/{1}/enroll resource invocation".format(request.method, hostname))
    form = RegisterForm(request.form)
    logger.error(form.errors)
    try:
        ca = caService.get_ca(hostname)
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if not form.validate():
                flash('Error:{}'.format(form.errors))
            ca.enroll_user(username=username, password=password)
            flash("user {0} enroll".format(username))
            return render_template('ca/camngt.html', form=form, ca=ca)
    except Exception as e:
        flash('Error: {}'.format(e))
    return render_template('ca/camngt.html', ca=ca)
