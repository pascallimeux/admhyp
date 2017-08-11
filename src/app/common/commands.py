import os
from app.common.log import get_logger
logger = get_logger()
from config import DEFAULTADMNAME, DEFAULTADMPWD


def build_folders(remotelogin):
   return ("mkdir -p /var/hyperledger/log " 
         "&& mkdir -p /var/hyperledger/.keys/admin " 
         "&& chown -R {0}.{0} /var/hyperledger "  
         "&& mkdir -p /opt/gopath/src/github.com/hyperledger " 
         "&& chown {0}.{0} /opt/gopath/src/github.com/hyperledger ".format(remotelogin))

def compress_locales_files_4_ca():
    return ("cd {0}/data && tar czf /tmp/files.tgz ./bin/fabric-ca-client "
           "./bin/fabric-ca-server ./conf/config.yaml ./conf/fabric-ca-client-config.yaml".format(os.getcwd()))

def compress_locales_files_4_peer():
    return ("cd {0}/data && tar czf /tmp/files.tgz ./bin/peer ".format(os.getcwd()))

def compress_locales_files_4_orderer():
    return ("cd {0}/data && tar czf /tmp/files.tgz ./bin/orderer ".format(os.getcwd()))

def uncompress_files():
    return "cd /var/hyperledger && tar xzf files.tgz && rm files.tgz"

def start_ca(admin_name=DEFAULTADMNAME, admin_pwd=DEFAULTADMPWD):
    return "cd /var/hyperledger && CMD=\"./bin/fabric-ca-server start -b {0}:'{1}' -c .keys/config.yaml > log/ca.log 2>&1 &\" && eval \"$CMD\"".format(admin_name, admin_pwd)

def start_peer(peer_name, peer_port=7051, mode="DEBUG"):
    return ("FABRIC_CFG_PATH=$PWD CORE_PEER_ID={0} CORE_PEER_ADDRESSAUTODETECT=true CORE_PEER_ADDRESS={0}:{1} " 
           "CORE_PEER_GOSSIP_EXTERNALENDPOINT={0}:{1} CORE_PEER_GOSSIP_ORGLEADER=false CORE_PEER_GOSSIP_USELEADERELECTION=true " 
           "CORE_PEER_GOSSIP_SKIPHANDSHAKE=true CORE_PEER_MSPCONFIGPATH=/var/hyperledger/msp CORE_PEER_LOCALMSPID=BlockChainCoCMSP CORE_LOGGING_LEVEL={2} "
           "/var/hyperledger/bin/peer node start".format(peer_name, peer_port, mode))

def start_orderer():
    return ("/var/hyperledger/bin/orderer")

def stop_process(process_name):
    return "kill -9 `pidof {0}` 2>/dev/null".format(process_name)

def is_started(process_name):
    return "PID=`pidof {0}` && [ -n \"$PID\" ] && echo True || echo False".format(process_name)

def is_deployed(type):
    return "[ -f /var/hyperledger/.deployed ] && cat /var/hyperledger/.deployed |grep {0} && echo True || echo False".format(type)

def write_deployed(type):
    return ("echo {0} installed $(date) >> /var/hyperledger/.deployed".format(type))

def uncompress_msp():
    return "cd /var/hyperledger && tar xzf msp.tgz -C /var/hyperledger/.keys && rm msp.tgz"

def compress_msp(nodename):
    return "cd /var/hyperledger/.keys && tar czf {0}.tgz admin {0}/*".format(nodename)

def register_admin(admin_name, admin_pwd):
    return ("cd /var/hyperledger"
            " && ./bin/fabric-ca-client register --id.name {0} --id.type client --id.affiliation org1.department1 --id.secret {1}".format(admin_name, admin_pwd))

def register_user(username, password):
    return ("cd /var/hyperledger"
            " && ./bin/fabric-ca-client register --id.name {0} --id.type user --id.affiliation org1.department1 --id.secret {1}".format(username, password))

def register_node(nodename, nodepwd):
    return ("cd /var/hyperledger"
            " && ./bin/fabric-ca-client register --id.name {0} --id.type peer --id.affiliation org1.department1 --id.secret {1}".format(nodename, nodepwd))


def enroll_admin(login, admin_name=DEFAULTADMNAME, admin_pwd=DEFAULTADMPWD):
    return ("cd /var/hyperledger "
            "&& ./bin/fabric-ca-client enroll -u http://{0}:'{1}'@localhost:7054 -c /var/hyperledger/.keys/admin/fabric-ca-client-config.yaml "
            "&& mkdir -p /home/{2}/.fabric-ca-client "
            "&& cp -R /var/hyperledger/.keys/admin/* /home/{2}/.fabric-ca-client".format(admin_name, admin_pwd,login))

def enroll_user(username, password):
    return ("mkdir -p /var/hyperledger/.msp/{0} "
            "&& cp /var/hyperledger/conf/fabric-ca-client-config.yaml /var/hyperledger/.msp/{0} "
            "&& cd /var/hyperledger"
            "&& ./bin/fabric-ca-client enroll -u http://{0}:'{1}'@localhost:7054 -c /var/hyperledger/.keys/{0}/fabric-ca-client-config.yaml ".format(username, password))

def enroll_node(username, password):
    return ("mkdir -p /var/hyperledger/.keys/{0} "
            "&& cp /var/hyperledger/conf/fabric-ca-client-config.yaml /var/hyperledger/.keys/{0} "
            "&& cd /var/hyperledger"
            "&& ./bin/fabric-ca-client enroll -u http://{0}:'{1}'@localhost:7054 -c /var/hyperledger/.keys/{0}/fabric-ca-client-config.yaml ".format(username, password))

def create_remote_admin(adminusername, username, pub_key):
    return ("useradd -m {0} -s /bin/bash "
            "|| echo  \"{0} ALL=(ALL:ALL) NOPASSWD:ALL\" >> /home/{1}/remoteadm "
            "&& sudo chown root.root /home/{1}/remoteadm "
            "&& sudo mv /home/{1}/remoteadm /etc/sudoers.d/{0} " 
            "&& sudo chmod ug-w /etc/sudoers.d/{0} "
            "&& sudo mkdir /home/{0}/.ssh "
            "|| sudo chmod 777 -R /home/{0}/.ssh "
            "&& sudo echo {2} >> /home/{0}/.ssh/authorized_keys "
            "&& sudo chown -R {0}.{0} /home/{0}/.ssh "
            "&& sudo chmod 700 /home/{0}/.ssh "
            "&& sudo chmod 600 /home/{0}/.ssh/authorized_keys").format(adminusername, username, pub_key)

def remote_file_4_download_msp(nodename):
    return "/var/hyperledger/.keys/{0}.tgz".format(nodename)

def remote_file_4_upload_msp():
    return "/var/hyperledger/msp.tgz"
