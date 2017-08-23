# -*- coding: utf-8 -*-
'''
Created on 6 july 2017
@author: pascal limeux
'''

from app.common.services import Services, ObjectNotFoundException
from app.orderer.model import Orderer
from app.database import get_session
from app.common.log import get_logger, log_function_call
logger = get_logger()
from app.agent.agentBuilder import deploy_Agent
from app.common.constants import NodeType
from config import appconf

class OrdererServices(Services):
    @log_function_call
    def create_orderer(self, name, hostname, remotepassword, remoteadmlogin=appconf().USERADM,
                  remotelogin=appconf().REMOTEUSERNAME, pub_key_file=appconf().PUBKEYFILE, key_file=appconf().KEYFILE,
                  broker_address=appconf().BROKERADDRESS, deploy=True):
        if deploy:
            try:
                deploy_Agent(agent_name=hostname, password=remotepassword, hostname=hostname, login=remotelogin,
                             broker_address=broker_address, pub_key_file=pub_key_file)
            except Exception as e:
                logger.error(e)
                raise Exception("Deploy agent failled! {}".format(e))
        try:
            orderer = Orderer(name=name, hostname=hostname, type=NodeType.ORDERER, login=remoteadmlogin, key_file=key_file )
            self.SaveRecord(orderer)
        except Exception as e:
            get_session().rollback()
            logger.error("{0}".format(e))
            raise Exception ("Data not record, database error!")

        return orderer

    @log_function_call
    def remove_orderer(self, name):
        objs = self.get_session().query(Orderer).filter(Orderer.name==name)
        ret = objs.delete()
        get_session().commit()
        return ret

    @log_function_call
    def get_orderer(self, name):
        orderer = Orderer.query.filter(Orderer.name == name).first()
        if orderer == None:
            raise ObjectNotFoundException("no orderer for name:{}".format(name))
        return orderer

    @log_function_call
    def get_orderers(self):
        return Orderer.query.all()

    @log_function_call
    def add_ca(self, name, ca):
        try:
            ca.register_node(nodename=name, password="pwd")
            ca.enroll_node(nodename=name, password="pwd")
            tgz = ca.get_msp(name=name)
            orderer = self.get_orderer(name)
            orderer.set_msp(tgz, name)
            orderer.ca = ca.id
            self.SaveRecord(orderer)
        except Exception as e:
            get_session().rollback()
            logger.error("{0}".format(e))
            raise Exception("Data not update, database error!")
        return orderer