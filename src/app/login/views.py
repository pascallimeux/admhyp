# -*- coding: utf-8 -*-
'''
Created on 29 june 2017
@author: pascal limeux
'''

from common.log import get_logger
logger = get_logger()
from flask import flash, Blueprint, session, g, request, redirect, url_for, render_template, Response
from app.login.forms import LoginForm
from app.login.services import UserServices
from functools import wraps
userServices = UserServices()

login_app = Blueprint('login_app',__name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            logger.info("Unhauthorized access from: {}".format(request.remote_addr))
            return render_template('errors/401.html'), 401
        return f(*args, **kwargs)
    return decorated_function

@login_app.route('/')
def home():
    logger.debug("home page started")
    if not session.get('logged_in'):
        return render_template('login/login.html')
    else:
        return render_template('main/home.html')

@login_app.route('/login', methods=['POST'])
def login():
    logger.debug("check credential for {}".format(str(request.form['username'])))
    try:
        result = userServices.CheckUser(username=str(request.form['username']),password=str(request.form['password']))
        if result:
            session['logged_in'] = True
            return home()
        else:
            logger.info("Unhauthorized access from: {}".format(request.remote_addr))
            return render_template('errors/401.html'), 401
    except Exception as e:
        logger.error(e)
        flash('wrong password!')


@login_app.route("/logout")
@login_required
def logout():
    logger.debug("logout")
    session['logged_in'] = False
    return home()

@login_app.route("/about")
@login_required
def about():
    logger.debug("about")
    return render_template('main/about.html')


@login_app.route("/register", methods=['GET', 'POST'])
@login_required
def register():
    logger.debug("register page started")
    form = LoginForm(request.form)
    if request.method == 'POST':
        try:
            if not form.validate():
                raise Exception (form.errors)
            username=request.form['name']
            password=request.form['password']
            email=request.form['email']
            userServices.CreateUser(email=email,username=username, password=password)
        except Exception as e:
            flash('Error: {}'.format(e))

        if form.validate():
            flash('Thanks for registration ' + username)
        else:
            flash('Error: All the form fields are required. ')
    return render_template('login/register.html', form=form)

