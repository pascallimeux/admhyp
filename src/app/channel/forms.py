# -*- coding: utf-8 -*-
'''
Created on 20 july 2017
@author: pascal limeux
'''

from wtforms import Form, validators, FieldList, StringField

class ChannelForm(Form):
    channelname = StringField('Channelname', validators=[validators.DataRequired()])
    ca_ids = FieldList(StringField('Ca'))
    orderer_ids = FieldList(StringField('Orderer'))
    peer_ids = FieldList(StringField('Peer'))