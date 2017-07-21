# -*- coding: utf-8 -*-
'''
Created on 7 july 2017
@author: pascal limeux
'''

from wtforms import Form, StringField, validators

class OrdererForm(Form):
    name = StringField('Name', validators=[validators.DataRequired()])
    hostname = StringField('Hostname', validators=[validators.DataRequired()])
    keyfile = StringField('Keyfile', validators=[validators.DataRequired()])
    pubkeyfile = StringField('Pubkeyfile', validators=[validators.DataRequired()])
    radmlogin = StringField('Radmlogin', validators=[validators.DataRequired()])
    rlogin = StringField('Rlogin', validators=[validators.DataRequired()])
    rpassword = StringField('Rpassword', validators=[validators.DataRequired()])

class MspForm(Form):
    caname = StringField('Ca_name', validators=[validators.DataRequired()])