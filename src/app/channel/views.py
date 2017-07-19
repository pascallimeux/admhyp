# -*- coding: utf-8 -*-
'''
Created on 29 june 2017
@author: pascal limeux
'''


from flask import request, Blueprint, session, render_template
from common.log import get_logger
logger = get_logger()
from app.login.views import login_required


channel_app = Blueprint('channel_app',__name__)


@channel_app.route("/channel", methods=['GET', 'POST'])
@login_required
def channel():
    logger.debug("{0} invocation on /channel resource".format(request.method))
    if session.get('logged_in'):
        return render_template('channel/channel.html')
    else:
        logger.info("Unauthorized access from ip:{}".format(request.remote_addr))
        return render_template('401.html')