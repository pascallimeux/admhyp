# -*- coding: utf-8 -*-
'''
Created on 3 july 2017
@author: pascal limeux
'''

import os
from flask import Flask, render_template, request
from app.database import get_session
from common.log import get_logger
logger = get_logger()

app = Flask(__name__, static_folder='static', template_folder="templates")
app_settings = os.getenv('APP_SETTINGS', 'config.DevelopmentConfig')
app.config.from_object(app_settings)

###################
### blueprints ####
###################
from app.local.views import local_app
from app.ca.views import ca_app
from app.channel.views import channel_app
from app.peer.views import peer_app
from app.orderer.views import orderer_app
from app.login.views import login_app
app.register_blueprint(login_app)
app.register_blueprint(ca_app)
app.register_blueprint(channel_app)
app.register_blueprint(local_app)
app.register_blueprint(orderer_app)
app.register_blueprint(peer_app)


########################
#### error handlers ####
########################

@app.errorhandler(401)
def not_authorized(error):
    logger.info("Unhauthorized access from: {}".format(request.remote_addr))
    return render_template('errors/401.html'), 401

@app.errorhandler(403)
def forbidden_page(error):
    return render_template("errors/403.html"), 403

@app.errorhandler(404)
def page_not_found(error):
    logger.info("Page not found")
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error_page(error):
    return render_template("errors/500.html"), 500

@app.teardown_appcontext
def shutdown_session(exception=None):
    get_session().remove()

#@app.before_request
def before_request():
    pass
