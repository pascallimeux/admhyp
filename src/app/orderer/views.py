
# -*- coding: utf-8 -*-
'''
Created on 29 june 2017
@author: pascal limeux
'''

from common.log import logging, LOG_LEVEL, log_handler
from flask import request, Blueprint, render_template, session
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)

orderer_app = Blueprint('orderer_app',__name__)


@orderer_app.route("/orderer", methods=['GET', 'POST'])
def orderer():
    logger.debug("{0} /orderer resource invocation".format(request.method))
    if session.get('logged_in'):
        return render_template('orderer.html')
    else:
        logger.info("Unauthorized access from ip:{}".format(request.remote_addr))
        return render_template('401.html')