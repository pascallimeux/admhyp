import os
from flask import Flask
from app.local.views import local_app
from app.ca.views import ca_app
from app.cluster.views import cluster_app
from app.peer.views import peer_app
from app.orderer.views import orderer_app
from app.login.views import login_app


def create_application(configfilename):
    app = Flask(__name__, static_folder='static', template_folder="templates")
    app.config.from_object(configfilename)

    app.register_blueprint(login_app)
    app.register_blueprint(ca_app)
    app.register_blueprint(cluster_app)
    app.register_blueprint(local_app)
    app.register_blueprint(orderer_app)
    app.register_blueprint(peer_app)

    app.secret_key = os.urandom(12)
    return app

