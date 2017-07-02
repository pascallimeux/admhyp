# -*- coding: utf-8 -*-
'''
Created on 29 june 2017
@author: pascal limeux
'''


from flask import request, Blueprint, session, render_template
from common.log import logging
logger = logging.getLogger(__name__)

cluster_app = Blueprint('cluster_app',__name__)


@cluster_app.route("/cluster", methods=['GET', 'POST'])
def cluster():
    logger.debug("{0} invocation on /cluster resource".format(request.method))
    if session.get('logged_in'):
        return render_template('cluster/cluster.html')
    else:
        logger.info("Unauthorized access from ip:{}".format(request.remote_addr))
        return render_template('401.html')