# -*- coding: utf-8 -*-
'''
Created on 29 june 2017
@author: pascal limeux
'''

import config

from app.database import db_session
from common.log import logging, LOG_LEVEL, log_handler
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)
from flask import flash, render_template, request, session, Blueprint
from app.login.forms import LoginForm
from app.login.services import UserServices

userServices = UserServices()

login_app = Blueprint('login_app',__name__)

@login_app.route('/')
def home():
    logger.debug("home page started")
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html')

@login_app.route('/login', methods=['POST'])
def do_admin_login():
    logger.debug("check credential for {}".format(str(request.form['username'])))
    try:
        result = userServices.CheckUser(username=str(request.form['username']),password=str(request.form['password']))
        if result:
            session['logged_in'] = True
            return home()
        else:
            return not_authorized()
    except Exception as e:
        logger.error(e)
        flash('wrong password!')


@login_app.route("/logout")
def logout():
    logger.debug("logout")
    session['logged_in'] = False
    return home()


@login_app.route("/register", methods=['GET', 'POST'])
def register():
    logger.debug("register page started")
    form = LoginForm(request.form)

    print (form.errors)
    if request.method == 'POST':
        username=request.form['name']
        password=request.form['password']
        email=request.form['email']
        try:
            userServices.CreateUser(email=email,username=username, password=password)
        except Exception as e:
            flash('Error: {}'.format(e))

        if form.validate():
            flash('Thanks for registration ' + username)
        else:
            flash('Error: All the form fields are required. ')

    return render_template('register.html', form=form)

@login_app.errorhandler(404)
def not_found():
    return render_template('404.html'), 404

@login_app.errorhandler(401)
def not_authorized():
    return render_template('401.html'), 401