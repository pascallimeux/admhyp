# -*- coding: utf-8 -*-
'''
Created on 30 june 2017
@author: pascal limeux
'''

from sqlalchemy import Column, String, ForeignKey
from app.node.model import Node
from app.common.constants import NodeType, NodeStatus
from common.log import get_logger
logger = get_logger()

class Ca(Node):
    __tablename__ = 'ca'
    id = Column(String, ForeignKey('node.hostname'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':NodeType.CA,
    }

    def get_type(self):
        return NodeType.CA

    def deploy(self):
        logger.debug ("Deploy a ca:{}".format(self.hostname))
        if self.is_deployed():
            raise Exception ("CA already deployeds!")
        self.setup_ca()
        self.enrollAdmin()

    def start(self):
        logger.debug ("Start a ca:{}".format(self.hostname))
        if self.is_started():
            raise Exception ("CA already started!")
        if not self.is_deployed():
            raise Exception ("CA is not deployed")
        self.exec_command("cd /var/hyperledger/scripts && ./start_ca.sh")


    def stop(self):
        logger.debug ("Stop a ca:{}".format(self.hostname))
        if not self.is_deployed():
            raise Exception ("CA not deployed!")
        if not self.is_started():
            raise Exception ("CA already stopped!")
        self.exec_command("cd /var/hyperledger/scripts && ./stop_ca.sh")


    def is_deployed(self):
        logger.debug ("Check if the ca:{} is deployed".format(self.hostname))
        #out, err = self.exec_command("cd /var/hyperledger/scripts && ./is_ca_deployed.sh")
        out, err = self.exec_command("[ -f /var/hyperledger/scripts/is_ca_started.sh ] && echo True || echo False")
        if "True" in out:
            logger.debug ("ca deployed")
            return True
        logger.debug ("ca not deployed")
        return False

    def is_started(self):
        logger.debug ("Check if the ca:{} is started".format(self.hostname))
        out, err = self.exec_command("cd /var/hyperledger/scripts && ./is_ca_started.sh")
        if "True" in out:
            logger.debug ("ca started")
            return True
        logger.debug ("ca not started")
        return False

    def setup_ca(self):
        out, err = self.exec_command("mkdir -p /var/hyperledger/log", sudo=True)
        out, err = self.exec_command("mkdir -p /var/hyperledger/scripts", sudo=True)
        out, err = self.exec_command("mkdir -p /var/hyperledger/.msp", sudo=True)
        out, err = self.exec_command("mkdir -p /var/hyperledger/.msp/admin", sudo=True)
        out, err = self.exec_command("chown -R "+self.login+"."+self.login+" /var/hyperledger", sudo=True)
        out, err = self.exec_command("mkdir -p opt/gopath/src/github.com/hyperledger", sudo=True)
        out, err = self.exec_command("chown " + self.login +"." + self.login +" opt/gopath/src/github.com/hyperledger", sudo=True)
        self.upload_file("./data/conf/config.yaml", "/var/hyperledger/.msp/config.yaml")
        self.upload_file("./data/conf/fabric-ca-client-config.yaml", "/var/hyperledger/.msp/admin/fabric-ca-config.yaml")
        self.upload_file("./data/bin/fabric-ca-server", "/var/hyperledger/fabric-ca-server")
        self.upload_file("./data/bin/fabric-ca-client", "/var/hyperledger/fabric-ca-client")
        self.upload_file("./data/scripts/start_ca.sh", "/var/hyperledger/scripts/start_ca.sh")
        self.upload_file("./data/scripts/stop_ca.sh", "/var/hyperledger/scripts/stop_ca.sh")
        self.upload_file("./data/scripts/is_ca_started.sh", "/var/hyperledger/scripts/is_ca_started.sh")
        out, err = self.exec_command("chmod u+x /var/hyperledger/fabric* /var/hyperledger/scripts/*.sh")

    def enrollAdmin(self):
        if not self.is_started():
            raise Exception ("ca not started!")
        out, err = self.exec_command("cd /var/hyperledger && ./fabric-ca-client enroll -u http://admin:'orange2017!'@localhost:7054 -c ./.msp/admin/fabric-ca-client-config.yaml")
        out, err = self.exec_command("mkdir -p /home/orangeadm/.fabric-ca-client")
        out, err = self.exec_command("cp -R /var/hyperledger/.msp/admin/* /home/orangeadm/.fabric-ca-client")
