# -*- coding: utf-8 -*-
'''
Created on 22 june 2017
@author: pascal limeux
'''

import paramiko
from config import appconf
from common.log import get_logger
logger = get_logger()

# used to display paramiko logs
#logging.getLogger("paramiko").setLevel(logging.DEBUG)
#paramiko.util.log_to_file("paramiko.log")


class BadParamersException(Exception):
    pass


class Ssh:
    client = None

    def __init__(self, hostname, username=appconf().USERADM, port=appconf().SSHDEFAULTPORT, password=None, key_file=None):
        logger.debug("SSH connection to {0}@{1}".format(username, hostname) )
        if hostname is None or username is None or (password is None and key_file is None):
            logger.error ("Error to init ssh, missing mandatory parameter!")
            raise BadParamersException()
        self.password = None
        self.port = port
        self.hostname = hostname
        self.username = username
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        if key_file is not None:
            self.key_file = key_file
            self.connect_from_key()
        else:
            self.password = password
            self.connect_from_login_pwd()

    def connect_from_login_pwd(self):
        try:
            self.client.load_system_host_keys()
            self.client.connect(self.hostname, self.port, self.username, self.password, timeout=appconf().SSHCNXTIMEOUT)
        except Exception as e:
            logger.error("fail to connect hostname:{0} port{1} username:{2} password:{3}".format(self.hostname, self.port, self.username, self.password))
            logger.error (e)
            raise Exception ("fail connection: {0} with login/password: {1}/{2}".format(self.hostname, self.username, self.password))

    def connect_from_key(self):
        try:
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(hostname=self.hostname, username=self.username, key_filename=self.key_file, timeout=appconf().SSHCNXTIMEOUT)
        except Exception as e:
            logger.error(e)
            raise Exception("fail connection: {0} with private key {1}".format(self.hostname, self.key_file))

    def exec_cmd(self, command, sudo=False):
        password = False
        if sudo:
            logger.debug ("Execute sudo command: {0} on {1}".format(command, self.hostname))
            command = "sudo -S -p '' {0}".format(command)
            password = self.password is not None and len(self.password) > 0
        else:
            logger.debug ("Execute command: {0} on {1}".format(command, self.hostname))
        stdin, stdout, stderr = self.client.exec_command(command)
        if password:
            stdin.write(self.password + "\n")
            stdin.flush()
        out = stdout.read().decode('utf-8')
        err = stderr.read().decode('utf-8')
        stdin.flush()
        if out != "":
            logger.debug ("OUT:{}".format(out))
        if err != "":
            logger.debug ("ERR:{}".format(err))
        return out, err

    def close_connection(self):
        logger.debug ("Close ssh connection with {0}".format(self.hostname))
        if self.client is not None:
            self.client.close()

    #used to display progress of transfert
    def print_totals(self, transferred, toBeTransferred):
        print ("Transferred: {0}\tOut of: {1}".format(transferred, toBeTransferred))

    def upload_file(self, localFile, remoteFile):
        logger.debug("Upload file from {0} to {1}:{2}".format(localFile, self.hostname, remoteFile))
        try:
            sftp = self.client.open_sftp()
            #sftp.put(localFile, remoteFile, callback=self.print_totals)
            sftp.put(localFile, remoteFile)
            sftp.close()
        except Exception as e:
            logger.error(e)
            raise Exception("error to upload file: {0} ".format(e))

    def download_file(self, remoteFile, localFile):
        logger.debug("Download file from {0}{1} to {2}".format(self.hostname, remoteFile, localFile))
        try:
            sftp = self.client.open_sftp()
            sftp.get(remoteFile,localFile)
            sftp.close()
        except Exception as e:
            logger.error(e)
            raise Exception("error to download file: {0} ".format(e))
