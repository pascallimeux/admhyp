# -*- coding: utf-8 -*-
'''
Created on 27 june 2017
@author: pascal limeux
'''
from db.model import get_session, drop_database, Server, Peer, Ca, Orderer, User
from collections import OrderedDict
from sqlalchemy.orm import class_mapper
from datetime import date
from sqlalchemy import or_
import bcrypt
from common.hashpwd import *
import config
from common.log import logging, LOG_LEVEL, log_handler
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)

class DB_Helper():
    def __init__(self):
        self.session = get_session()

    def Drop_db(self):
        logger.debug("drop database")
        drop_database()

    def CreateUser(self, data):
        try:
            user = User(email=data['email'], username=data['username'], password=hash_password(data['password']) )
            self.__saveRecord(user)
        except Exception as e:
            self.session.rollback()
            logger.error("{0}".format(e))
        return data

    def CheckUser(self, data):
        username = data['username']
        password = data['password']
        rows = self.session.query(User).filter(User.username==username).count()
        if rows == 1:
            user = self.session.query(User).filter(User.username==username)[0]
            if check_password(user.password, password):
                return True
        return False

    def CreatePeer(self, data):
        try:
            peer = Peer(hostname=data['hostname'], type=ServerType.PEER, login=data['login'], key_file=data['key_file'] )
            self.__saveRecord(peer)
        except Exception as e:
            self.session.rollback()
            logger.error("{0}".format(e))
        return data

    def CreateCa(self, data):
        try:
            ca = Ca(hostname=data['hostname'], type=ServerType.CA, login=data['login'], key_file=data['key_file'] )
            self.__saveRecord(ca)
        except Exception as e:
            self.session.rollback()
            logger.error("{0}".format(e))
        return data

    def CreateOrderer(self, data):
        try:
            orderer = Orderer(hostname=data['hostname'], type=ServerType.ORDERER, login=data['login'], key_file=data['key_file'] )
            self.__saveRecord(orderer)
        except Exception as e:
            self.session.rollback()
            logger.error("{0}".format(e))
        return data

    def RemovePeer(self, hostname):
        objs = self.session.query(Peer).filter(Peer.hostname==hostname)
        ret = objs.delete()
        self.session.commit()
        return ret

    def RemoveCa(self, hostname):
        objs = self.session.query(Ca).filter(Peer.hostname==hostname)
        ret = objs.delete()
        self.session.commit()
        return ret

    def RemoveOrderer(self, hostname):
        objs = self.session.query(Orderer).filter(Peer.hostname==hostname)
        ret = objs.delete()
        self.session.commit()
        return ret

    def getPeer(self, hostname):
        rows = self.session.query(Peer).filter(Peer.hostname==hostname).count()
        if rows == 1:
            obj = self.session.query(Peer).filter_by(hostname = hostname)[0]
            return self.__obj_unique(obj)
        return None

    def getCa(self, hostname):
        rows = self.session.query(Ca).filter(Peer.hostname==hostname).count()
        if rows == 1:
            obj = self.session.query(Ca).filter_by(hostname = hostname)[0]
            return self.__obj_unique(obj)
        return None

    def getOrderer(self, hostname):
        rows = self.session.query(Orderer).filter(Peer.hostname==hostname).count()
        if rows == 1:
            obj = self.session.query(Orderer).filter_by(hostname = hostname)[0]
            return self.__obj_unique(obj)
        return None

    def getServers(self):
        try:
            objs = self.session.query(Server).all()
            objs_dict=[]
            for obj in objs:
                obj_dict=model_to_dict(obj)
                objs_dict.append(obj_dict)
            return objs_dict
        except Exception as e:
            print (e)

    def __unique_items_list(self, objs, key):
        objects=[]
        liste=[]
        for obj in objs:
            objects.append( getattr(obj, key))
        for value in list(OrderedDict.fromkeys(objects)) :
            obj="{"+"\"{0}\":\"{1}\"".format(key,  value)+"}"
            liste.append(obj)
        return liste

    def __objs_list(self, objs):
        items=[]
        for obj in objs:
            obj_dict=model_to_dict(obj)
            items.append(obj_dict)
        return items

    def __obj_unique(self, obj):
        return model_to_dict(obj)

    def __saveRecord(self, obj):
        try:
            self.session.add(obj)
            self.session.commit()
        except Exception as e:
            logger.error(str(e))
            raise e

    def __saveRecords(self, objs):
        for obj in objs:
            self.__saveRecord(obj)

    def __updateRecord(self, obj, Class):
        dic= ({column: getattr(obj, column) for column in Class.__table__.columns.keys()})
        atts = {}
        for key in dic.keys():
            if not dic.get(key)==None:
                atts[key]=dic[key]
        self.session.query(Class).filter_by(id=obj.id).update(atts)
        self.session.commit()


def model_to_dict(obj, visited_children=None, back_relationships=None):
    if visited_children is None:
        visited_children = set()
    if back_relationships is None:
        back_relationships = set()
    serialized_data = {c.key: getattr(obj, c.key) for c in obj.__table__.columns}
    relationships = class_mapper(obj.__class__).relationships
    visitable_relationships = [(name, rel) for name, rel in relationships.items() if name not in back_relationships]
    for name, relation in visitable_relationships:
        if relation.backref:
            back_relationships.add(relation.backref)
        relationship_children = getattr(obj, name)
        if relationship_children is not None:
            if relation.uselist:
                children = []
                for child in [c for c in relationship_children if c not in visited_children]:
                    visited_children.add(child)
                    children.append(model_to_dict(child, visited_children, back_relationships))
                serialized_data[name] = children
            else:
                serialized_data[name] = model_to_dict(relationship_children, visited_children, back_relationships)
    return serialized_data
