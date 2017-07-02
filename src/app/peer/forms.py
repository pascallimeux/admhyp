# -*- coding: utf-8 -*-
'''
Created on 30 june 2017
@author: pascal limeux
'''

from wtforms import Form, TextField, validators

class PeerForm(Form):
    hostname = TextField('Hostname', validators=[validators.DataRequired()])
    keyfile = TextField('Keyfile', validators=[validators.DataRequired()])
    pubkeyfile = TextField('Pubkeyfile', validators=[validators.DataRequired()])
    radmlogin = TextField('Radmlogin', validators=[validators.DataRequired()])
    rlogin = TextField('Rlogin', validators=[validators.DataRequired()])
    rpassword = TextField('Rpassword', validators=[validators.DataRequired()])
