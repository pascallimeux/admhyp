import os
from common.log import get_logger
logger = get_logger()
from config import DEFAULTADMNAME, DEFAULTADMPWD
def build_folders(remotelogin):
   return ("mkdir -p /var/hyperledger/log " 
         "&& mkdir -p /var/hyperledger/.msp/admin " 
         "&& chown -R {0}.{0} /var/hyperledger "  
         "&& mkdir -p /opt/gopath/src/github.com/hyperledger " 
         "&& chown {0}.{0} /opt/gopath/src/github.com/hyperledger ".format(remotelogin))

def compress_locales_files_4_ca():
    return ("cd {0}/data && tar czf /tmp/files.tgz ./bin/ca/fabric-ca-client "
           "./bin/ca/fabric-ca-server ./conf/config.yaml ./conf/fabric-ca-client-config.yaml".format(os.getcwd()))

def uncompress_ca_files():
    return "cd /var/hyperledger && tar xzf files.tgz && rm files.tgz"

def start_ca(admin_name=DEFAULTADMNAME, admin_pwd=DEFAULTADMPWD):
    logger.warning("CA started with default credentials!")
    return "cd /var/hyperledger && CMD=\"./bin/ca/fabric-ca-server start -b {0}:'{1}' -c .msp/config.yaml > log/ca.log 2>&1 &\" && eval \"$CMD\"".format(admin_name, admin_pwd)

def stop_ca():
    return "kill -9 `pidof fabric-ca-server` 2>/dev/null && kill -9 `pidof fabric-ca-client` 2>/dev/null"

def is_ca_started():
    return "PID=`pidof fabric-ca-server` && [ -n \"$PID\" ] && echo True || echo False"

def is_deployed(type):
    return "[ -f /var/hyperledger/.deployed ] && /var/hyperledger/.deployed |grep {0} && echo True || echo False".format(type)

def write_deployed(type):
    return ("echo {0} installed $(date) > /var/hyperledger/.deployed".format(type))

def uncompress_msp(nodename):
    return "cd /var/hyperledger && tar xzf {0}.tgz -C /var/hyperledger/{0} && rm {0}.tgz".format(nodename)

def compress_msp(nodename):
    return "cd /var/hyperledger/.msp/{0} && tar czf {0}.tgz *".format(nodename)

def register_admin(admin_name, admin_pwd):
    return ("cd /var/hyperledger"
            " && ./bin/ca/fabric-ca-client register --id.name {0} --id.type client --id.affiliation org1.department1 --id.secret {1}".format(admin_name, admin_pwd))

def register_user(username, password):
    return ("cd /var/hyperledger"
            " && ./bin/ca/fabric-ca-client register --id.name {0} --id.type user --id.affiliation org1.department1 --id.secret {1}".format(username, password))

def register_node(nodename, nodepwd):
    return ("cd /var/hyperledger"
            " && ./bin/ca/fabric-ca-client register --id.name {0} --id.type peer --id.affiliation org1.department1 --id.secret {1}".format(nodename, nodepwd))


def enroll_admin(login, admin_name=DEFAULTADMNAME, admin_pwd=DEFAULTADMPWD):
    return ("cd /var/hyperledger "
            "&& ./bin/ca/fabric-ca-client enroll -u http://{0}:'{1}'@localhost:7054 -c /var/hyperledger/.msp/admin/fabric-ca-client-config.yaml "
            "&& mkdir -p /home/{2}/.fabric-ca-client "
            "&& cp -R /var/hyperledger/.msp/admin/* /home/{2}/.fabric-ca-client".format(admin_name, admin_pwd,login))

def enroll_user(username, password):
    return ("mkdir -p /var/hyperledger/.msp/{0} "
            "&& cp /var/hyperledger/conf/fabric-ca-client-config.yaml /var/hyperledger/.msp/{0} "
            "&& cd /var/hyperledger"
            "&& ./bin/ca/fabric-ca-client enroll -u http://{0}:'{1}'@localhost:7054 -c /var/hyperledger/.msp/{0}/fabric-ca-client-config.yaml ".format(username, password))

def enroll_node(username, password):
    return ("mkdir -p /var/hyperledger/.msp/{0} "
            "&& cp /var/hyperledger/conf/fabric-ca-client-config.yaml /var/hyperledger/.msp/{0} "
            "&& cd /var/hyperledger"
            "&& ./bin/ca/fabric-ca-client enroll -u http://{0}:'{1}'@localhost:7054 -c /var/hyperledger/.msp/{0}/fabric-ca-client-config.yaml ".format(username, password))
