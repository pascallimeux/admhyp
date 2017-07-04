# -*- coding: utf-8 -*-
'''
Created on 26 june 2017
@author: pascal limeux
'''
import config
import logging
from common.ssh import Ssh
from common.log import get_logger
logger = get_logger()

class Node:

    def __init__(self, hostname, key_file, type, remoteAdmin):
        self.type = type
        self.hostname    = hostname
        self.remoteAdmin = remoteAdmin
        self.key_file = key_file
        self.isConnect = False

    def __str__(self):
        str = "Server: {0}".format(self.hostname)
        str = str + " Remote Login: {0}".format(self.remoteAdmin)
        str = str + " Key file: {0}".format(self.key_file)
        if self.isConnect:
            connect = " is connected"
        else:
            connect = "is not connected!"
        str = str + connect
        return str

    def Connect(self):
        try:
            self.ssh = Ssh(hostname=self.hostname, username=self.remoteAdmin, key_file=self.key_file)
            self.isConnect = True
        except Exception as e:
            logger.error("{0}".format(e))

    def IsConnect():
        return self.isConnect

    def IsInstalled():
        pass

    def IsStarted():
        pass

    def Close():
        self.ssh.CloseConnection()

    def UpdateSystem(self):
        logger.info ("Update system in {}".format(self.hostname))
        out, err = self.ssh.ExecCmd("apt update", sudo=True)
        out, err = self.ssh.ExecCmd("apt upgrade -y", sudo=True)
        out, err = self.ssh.ExecCmd("apt install tree -y", sudo=True)

    def CreateHyperledgerFolders(self):
        logger.info ("Create hyperledger folders in {}".format(self.hostname))
        out, err = self.ssh.ExecCmd("mkdir -p /var/hyperledger", sudo=True)
        out, err = self.ssh.ExecCmd("chown "+self.remoteAdmin+"."+self.remoteAdmin+" /var/hyperledger", sudo=True)
        out, err = self.ssh.ExecCmd("mkdir -p " + config.GOPATH + "/src/github.com/hyperledger", sudo=True)
        out, err = self.ssh.ExecCmd("chown " + self.remoteAdmin +"." + self.remoteAdmin +" " + src.config.GOPATH + "/src/github.com/hyperledger", sudo=True)

    def GetBinaries(self):
        logger.info ("GetBinaries to {}".format(self.hostname))
        self.ssh.UploadFile(src.config.TGZREPO + config.TGZBINNAME, "/var/hyperledger/" + src.config.TGZBINNAME)
        logger.debug ("sudo tar xzvf /var/hyperledger/" + config.TGZBINNAME + " -C /var/hyperledger/")
        out, err = self.ssh.ExecCmd("sudo tar xzvf /var/hyperledger/" + config.TGZBINNAME + " -C /var/hyperledger/")

    def SendLogs(self):
        logger.info ("Send logs from {}".format(self.hostname))
        self.ssh.DownloadFile("/tmp/toto", "/tmp/titi")

class Peer(Node):
    def __init__(self, hostname, key_file, type, remoteAdmin):
        super().__init__(hostname, key_file, type, remoteAdmin)
        self.helper.CreatePeer(data={'hostname':hostname, 'key_file':key_file, 'login':remoteAdmin})

class Orderer(Node):
    def __init__(self, hostname, key_file, type, remoteAdmin):
        super().__init__(hostname, key_file, type, remoteAdmin)
        self.helper.CreateOrderer(data={'hostname':hostname, 'key_file':key_file, 'login':remoteAdmin})

class Ca(Node):
    def __init__(self, hostname, key_file, type, remoteAdmin):
        super().__init__(hostname, key_file, type, remoteAdmin)
        self.helper.CreateCa(data={'hostname':hostname, 'key_file':key_file, 'login':remoteAdmin})

    def RegisterPeer(server):
        pass

    def EnrollPeer(server):
        pass

    def RegisterUser(username):
        pass

    def EnrollUser(username):
        pass
