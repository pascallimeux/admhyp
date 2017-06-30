# -*- coding: utf-8 -*-
'''
Created on 29 june 2017
@author: pascal limeux
'''

from common.log import logging, LOG_LEVEL, log_handler
from flask import request, render_template, session
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)


def Check_authorized_access(**kwargs):
    page = kwargs.pop('page')
    form = kwargs.pop('form')
    logger.debug("page={0} form={1}".format(page, form))
    if session.get('logged_in'):
        return render_template(page, form=form)
    else:
        logger.info("Unauthorized access from ip:{}".format(request.remote_addr))
        return render_template('401.html')