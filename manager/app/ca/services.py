# -*- coding: utf-8 -*-
'''
Created on 30 june 2017
@author: pascal limeux
'''
from app.common.services import Services, ObjectNotFoundException
from app.agent.agentBuilder import deploy_Agent
from app.agent.agentManager import AgentManager
from app.common.commands import compress_locales_files_4_ca, start_ca
from app.common.lcmds import exec_local_cmd
from app.agent.message.messages import OrderType
from app.ca.model import Ca
from app.database import get_session
from app.common.log import get_logger, log_function_call
logger = get_logger()
from app.common.constants import NodeType
from config import appconf

class CaServices(Services):

    @log_function_call
    def create_ca(self, name, hostname, remotepassword, remoteadmlogin=appconf().USERADM, remotelogin=appconf().REMOTEUSERNAME, pub_key_file=appconf().PUBKEYFILE, key_file=appconf().KEYFILE, broker_address=appconf().BROKERADDRESS, deploy=True):
        if deploy:
            try:
                deploy_Agent(agent_name=hostname, password=remotepassword, hostname=hostname, login=remotelogin, broker_address=broker_address, pub_key_file=pub_key_file)
            except Exception as e:
                logger.error(e)
                raise Exception("Deploy agent failled! {}".format(e))
        try:
            ca = Ca(name=name, hostname=hostname, type=NodeType.CA, login=remoteadmlogin, key_file=key_file)
            self.SaveRecord(ca)
        except Exception as e:
            get_session().rollback()
            logger.error("{0}".format(e))
            raise Exception("Data not record, database error!")
        return ca

    @log_function_call
    def remove_ca(self, name):
        objs = self.get_session().query(Ca).filter(Ca.name == name)
        ret = objs.delete()
        get_session().commit()
        return ret

    @log_function_call
    def get_ca(self, name):
        ca = Ca.query.filter(Ca.name == name).first()
        if ca == None:
            raise ObjectNotFoundException("no ca for name:{}".format(name))
        return ca

    @log_function_call
    def get_cas(self):
        return Ca.query.all()

    @log_function_call
    def deploy_ca(self, name):
        ca = self.get_ca(name=name)
        agent_manager = AgentManager()
        agent_manager.deployca(agent_name=ca.hostname)

    @log_function_call
    def start_ca(self, name):
        ca = self.get_ca(name=name)
        agent_manager = AgentManager()
        agent_manager.startca(agent_name=ca.hostname)

    @log_function_call
    def stop_ca(self, name):
        ca = self.get_ca(name=name)
        agent_manager = AgentManager()
        agent_manager.stopca(agent_name=ca.hostname)

    @log_function_call
    def register_admin(self, name, admname, admpwd):
        ca = self.get_ca(name=name)
        agent_manager = AgentManager()
        agent_manager.register_admin(agent_name=ca.hostname, adm_name=admname, adm_pwd=admpwd)


    @log_function_call
    def register_user(self, name, username, userpwd):
        ca = self.get_ca(name=name)
        agent_manager = AgentManager()
        agent_manager.register_user(agent_name=ca.hostname, username=username, pwd=userpwd )


    @log_function_call
    def register_node(self, name, nodename, nodepwd):
        ca = self.get_ca(name=name)
        agent_manager = AgentManager()
        agent_manager.register_node(agent_name=ca.hostname, nodename=nodename, nodepwd=nodepwd)


    @log_function_call
    def enroll_admin(self, name, admname, admpwd, login):
        ca = self.get_ca(name=name)
        agent_manager = AgentManager()
        agent_manager.enroll_admin(agent_name=ca.hostname, adm_name=admname, adm_pwd=admpwd, login=login)


    @log_function_call
    def enroll_user(self, name, username, userpwd):
        ca = self.get_ca(name=name)
        agent_manager = AgentManager()
        agent_manager.enroll_user(agent_name=ca.hostname, username=username, pwd=userpwd )


    @log_function_call
    def enroll_node(self, name, nodename, nodepwd):
        ca = self.get_ca(name=name)
        agent_manager = AgentManager()
        agent_manager.enroll_node(agent_name=ca.hostname, nodename=nodename, nodepwd=nodepwd)

