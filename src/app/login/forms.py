# -*- coding: utf-8 -*-
'''
Created on 29 june 2017
@author: pascal limeux
'''

from wtforms import Form, StringField, validators

class LoginForm(Form):
    name = StringField('Name:', validators=[validators.required()])
    email = StringField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])
    password = StringField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])
