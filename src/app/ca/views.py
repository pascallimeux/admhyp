# -*- coding: utf-8 -*-
'''
Created on 29 june 2017
@author: pascal limeux
'''


from flask import request, Blueprint, render_template, session
from app.login.views import login_required
from common.log import get_logger
logger = get_logger()
ca_app = Blueprint('ca_app',__name__)


@ca_app.route("/ca", methods=['GET', 'POST'])
@login_required
def ca():
    logger.debug("{0} /ca resource invocation".format(request.method))
    if session.get('logged_in'):
        return render_template('ca/ca.html')
    else:
        logger.info("Unauthorized access from ip:{}".format(request.remote_addr))
        return render_template('401.html')
