import os
from flask import Flask, session, request
from app.local.views import local_app
from app.ca.views import ca_app
from app.cluster.views import cluster_app
from app.peer.views import peer_app
from app.orderer.views import orderer_app
from app.login.views import login_app
from flask import render_template
from app.database import get_session
from common.log import logging, LOG_LEVEL, log_handler

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)

app = Flask(__name__, static_folder='static', template_folder="templates")
app.config.from_object('config')

app.register_blueprint(login_app)
app.register_blueprint(ca_app)
app.register_blueprint(cluster_app)
app.register_blueprint(local_app)
app.register_blueprint(orderer_app)
app.register_blueprint(peer_app)

app.secret_key = os.urandom(12)

@app.errorhandler(404)
def page_not_found(exception):
    #logger.info("Not found page "+ str(exception))
    return render_template('404.html'), 404

@app.errorhandler(401)
def not_authorized(exception):
    #logger.info("Not authorized page "+ str(exception))
    return render_template('401.html'), 401

@app.teardown_appcontext
def shutdown_session(exception=None):
    #logger.info("shutdown db_session "+ str(exception))
    get_session().remove()

@app.before_request
def before_request():
    endpoint = request.endpoint
    authorized_endpoints=['login_app.home', 'login_app.do_admin_login']
    if endpoint not in authorized_endpoints:
        if not session.get('logged_in'):
            logger.debug (request.endpoint)
            logger.info("Unauthorized access from ip:{} ".format(request.remote_addr))
            return render_template('401.html')