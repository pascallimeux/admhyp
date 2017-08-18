# -*- coding: utf-8 -*-
'''
Created on 6 july 2017
@author: pascal limeux
'''


from flask import flash, request, Blueprint, render_template
from app.ca.forms import CaForm, RegisterForm
from app.ca.services import CaServices
from app.common.log import get_logger
from app.login.views import login_required

logger = get_logger()
ca_app = Blueprint('ca_app',__name__)

caService = CaServices()


@ca_app.route("/ca", methods=['GET', 'POST'])
@login_required
def create():
    logger.debug("Invoke API: {0} /ca".format(request.method))
    form = CaForm(request.form)
    if request.method == 'POST':
        name=request.form['name']
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
            caService.create_ca(name=name, hostname=hostname, remoteadmlogin=remoteadmlogin,  remotepassword=remotepassword, remotelogin=remotelogin, pub_key_file=pub_key_file, key_file=key_file)
            flash("new ca created: (name={0})".format(name))
        except Exception as e:
            flash('Error: {}'.format(e))
    return render_template('ca/ca.html', form=form)

@ca_app.route("/cas")
@login_required
def list():
    logger.debug("Invoke API: {0} /cas".format(request.method))
    try:
        cas = caService.get_cas()
    except Exception as e:
        flash('Error: {}'.format(e))
    return render_template('ca/cas.html', cas=cas)

@ca_app.route("/ca/<name>", methods=['GET', 'POST'])
@login_required
def manage(name):
    logger.debug("Invoke API: {0} /ca/{1}".format(request.method, name))
    try:
        ca = caService.get_ca(name)
    except Exception as e:
        flash('Error: {}'.format(e))
        return render_template('main/home.html')
    return render_template('ca/camngt.html', ca=ca)

@ca_app.route("/ca/<name>/deploy")
@login_required
def deploy(name):
    logger.debug("Invoke API: {0} /ca/{1}/deploy".format(request.method, name))
    try:
        ca = caService.get_ca(name)
        ca.deploy()
    except Exception as e:
        flash('Error: {}'.format(e))
    return render_template('ca/camngt.html', ca=ca)

@ca_app.route("/ca/<name>/start")
@login_required
def start(name):
    logger.debug("Invoke API: {0} /ca/{1}/start".format(request.method, name))
    try:
        ca = caService.get_ca(name)
        ca.start()
    except Exception as e:
        flash('Error: {}'.format(e))
    return render_template('ca/camngt.html', ca=ca)

@ca_app.route("/ca/<name>/stop")
@login_required
def stop(name):
    logger.debug("Invoke API: {0} /ca/{1}/stop".format(request.method, name))
    try:
        ca = caService.get_ca(name)
        ca.stop()
    except Exception as e:
        flash('Error: {}'.format(e))
    return render_template('ca/camngt.html', ca=ca)

@ca_app.route("/ca/<name>/register", methods=['GET', 'POST'])
@login_required
def register(name):
    logger.debug("Invoke API: {0} /ca/{1}/register".format(request.method, name))
    form = RegisterForm(request.form)
    logger.error(form.errors)
    try:
        ca = caService.get_ca(name)
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

@ca_app.route("/ca/<name>/createadmin", methods=['GET', 'POST'])
@login_required
def create_admin(name):
    logger.debug("Invoke API: {0} /ca/{1}/createadmin".format(request.method, name))
    form = RegisterForm(request.form)
    logger.error(form.errors)
    try:
        ca = caService.get_ca(name)
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

@ca_app.route("/ca/<name>/enroll", methods=['GET', 'POST'])
@login_required
def enroll(name):
    logger.debug("Invoke API: {0} /ca/{1}/enroll".format(request.method, name))
    form = RegisterForm(request.form)
    logger.error(form.errors)
    try:
        ca = caService.get_ca(name)
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
