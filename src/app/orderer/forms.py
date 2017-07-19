# -*- coding: utf-8 -*-
'''
Created on 7 july 2017
@author: pascal limeux
'''

from wtforms import Form, TextField, validators

class OrdererForm(Form):
    hostname = TextField('Hostname', validators=[validators.DataRequired()])
    keyfile = TextField('Keyfile', validators=[validators.DataRequired()])
    pubkeyfile = TextField('Pubkeyfile', validators=[validators.DataRequired()])
    radmlogin = TextField('Radmlogin', validators=[validators.DataRequired()])
    rlogin = TextField('Rlogin', validators=[validators.DataRequired()])
    rpassword = TextField('Rpassword', validators=[validators.DataRequired()])

class MspForm(Form):
    cahostname = TextField('Ca_hostname', validators=[validators.DataRequired()])