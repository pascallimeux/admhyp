# -*- coding: utf-8 -*-
'''
Created on 22 june 2017
@author: pascal limeux
'''

from app.common.ssh import Ssh
from app.common.commands import create_remote_admin
from app.common.log import get_logger
from config import appconf
logger = get_logger()


def create_remote_connection(hostname, password, username=appconf().REMOTEUSERNAME, pub_key_file=appconf().PUBKEYFILE, adminusername=appconf().USERADM):
    logger.info("create a remote admin: hostname:{0}, adminusername:{1},  pub_key_file:{2}".format(hostname, adminusername, pub_key_file))
    ssh = None
    try:
        ssh = Ssh(hostname=hostname, username=username, password=password)
        logger.info(" Execute remote commands on: {0} with login: {1} password:{2}".format(hostname, username, password))
        pub_key = open(pub_key_file, 'r').read()
        pub_key= "\""+pub_key+"\""
        cmd = create_remote_admin(adminusername, username, pub_key)
        logger.debug ("----EXEC: {} EXEC----".format(cmd))
        ssh.exec_cmd(cmd, sudo=True)
    finally:
        if ssh:
            ssh.close_connection()

def check_ssh_admin_connection(hostname, remoteadminlogin, key_file):
    ssh = None
    try:
        ssh = Ssh(hostname=hostname, username=remoteadminlogin, key_file=key_file)
        out, err = ssh.exec_cmd("ls ", sudo=True)
        logger.debug("out:{0}  err: {1}".format(out, err))
        if err.strip() != "":
            return False
        return True
    except Exception as e:
        logger.error(e)
        return False
    finally:
        if ssh is not None:
            ssh.close_connection()