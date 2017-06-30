# -*- coding: utf-8 -*-
'''
Created on 22 june 2017
@author: pascal limeux
'''

import logging
import config
from common.ssh import Ssh
from common.log import LOG_LEVEL, log_handler
import config
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)

def CreateRemoteAdmin(hostname, password, username=config.REMOTEUSERNAME, pub_key_file=config.PUBKEYFILE, adminusername=config.USERADM):
    logger.info("create a remote admin: hostname:{0}, adminusername:{1},  pub_key_file:{2}".format(hostname, adminusername, pub_key_file))
    try:
        ssh = Ssh(hostname=hostname, username=username, password=password)
        logger.info(" Execute remote commands on: {0} with login: {1} password:{2}".format(hostname, username, password))
        ssh.ExecCmd("useradd -m " + adminusername + " -s /bin/bash", sudo=True)
        sudoersline="\""+adminusername +" ALL=(ALL:ALL) NOPASSWD:ALL\""
        ssh.ExecCmd("echo  " + sudoersline + " >> /home/"+username+"/"+"remoteadm", sudo=True)
        ssh.ExecCmd("chown root.root /home/"+username+"/"+"remoteadm", sudo=True)
        ssh.ExecCmd("mv /home/"+username+"/"+"remoteadm" " /etc/sudoers.d/"+adminusername, sudo=True)
        ssh.ExecCmd("chmod ug-w /etc/sudoers.d/"+adminusername, sudo=True)
        ssh.ExecCmd("mkdir /home/"+adminusername+"/.ssh", sudo=True)
        ssh.ExecCmd("chmod 777 -R /home/"+adminusername+"/.ssh", sudo=True)
        pub_key = open(pub_key_file, 'r').read()
        pub_key= "\""+pub_key+"\""
        ssh.ExecCmd("echo "+pub_key+" >> /home/"+adminusername+"/.ssh/authorized_keys", sudo=True)
        ssh.ExecCmd("chown -R "+adminusername+"."+adminusername+" /home/"+adminusername+"/.ssh", sudo=True)
        ssh.ExecCmd("chmod 700 /home/"+adminusername+"/.ssh", sudo=True)
        ssh.ExecCmd("chmod 600 /home/"+adminusername+"/.ssh/authorized_keys", sudo=True)
    finally:
        ssh.CloseConnection()