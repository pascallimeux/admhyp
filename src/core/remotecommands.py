# -*- coding: utf-8 -*-
'''
Created on 22 june 2017
@author: pascal limeux
'''

from common.ssh import Ssh
from config import appconf
from common.log import get_logger
logger = get_logger()


def create_remote_admin(hostname, password, username=appconf().REMOTEUSERNAME, pub_key_file=appconf().PUBKEYFILE, adminusername=appconf().USERADM):
    logger.info("create a remote admin: hostname:{0}, adminusername:{1},  pub_key_file:{2}".format(hostname, adminusername, pub_key_file))
    try:
        ssh = Ssh(hostname=hostname, username=username, password=password)
        logger.info(" Execute remote commands on: {0} with login: {1} password:{2}".format(hostname, username, password))
        ssh.exec_cmd("useradd -m " + adminusername + " -s /bin/bash", sudo=True)
        sudoersline="\""+adminusername +" ALL=(ALL:ALL) NOPASSWD:ALL\""
        ssh.exec_cmd("echo  " + sudoersline + " >> /home/"+username+"/"+"remoteadm", sudo=True)
        ssh.exec_cmd("chown root.root /home/"+username+"/"+"remoteadm", sudo=True)
        ssh.exec_cmd("mv /home/"+username+"/"+"remoteadm" " /etc/sudoers.d/"+adminusername, sudo=True)
        ssh.exec_cmd("chmod ug-w /etc/sudoers.d/"+adminusername, sudo=True)
        ssh.exec_cmd("mkdir /home/"+adminusername+"/.ssh", sudo=True)
        ssh.exec_cmd("chmod 777 -R /home/"+adminusername+"/.ssh", sudo=True)
        pub_key = open(pub_key_file, 'r').read()
        pub_key= "\""+pub_key+"\""
        ssh.exec_cmd("echo "+pub_key+" >> /home/"+adminusername+"/.ssh/authorized_keys", sudo=True)
        ssh.exec_cmd("chown -R "+adminusername+"."+adminusername+" /home/"+adminusername+"/.ssh", sudo=True)
        ssh.exec_cmd("chmod 700 /home/"+adminusername+"/.ssh", sudo=True)
        ssh.exec_cmd("chmod 600 /home/"+adminusername+"/.ssh/authorized_keys", sudo=True)
    finally:
        ssh.CloseConnection()

def check_ssh_admin_connection(hostname, remoteadminlogin, key_file):
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
        ssh.close_connection()