# -*- coding: utf-8 -*-
'''
Created on 29 june 2017
@author: pascal limeux
'''

from common.log import logging, LOG_LEVEL, log_handler
from flask import request, Blueprint, session, render_template
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)

local_app = Blueprint('local_app',__name__)


@local_app.route("/local", methods=['GET', 'POST'])
def local():
    logger.debug("{0} invocation on /local resource".format(request.method))
    if session.get('logged_in'):
        return render_template('local.html')
    else:
        logger.info("Unauthorized access from ip:{}".format(request.remote_addr))
        return render_template('401.html')