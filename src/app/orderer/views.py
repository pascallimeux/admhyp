
# -*- coding: utf-8 -*-
'''
Created on 29 june 2017
@author: pascal limeux
'''

from flask import request, Blueprint, render_template, session
from common.log import logging
logger = logging.getLogger(__name__)

orderer_app = Blueprint('orderer_app',__name__)


@orderer_app.route("/orderermenu", methods=['GET', 'POST'])
def orderer():
    logger.debug("{0} /orderer resource invocation".format(request.method))
    if session.get('logged_in'):
        return render_template('orderer/orderer.html')
    else:
        logger.info("Unauthorized access from ip:{}".format(request.remote_addr))
        return render_template('401.html')