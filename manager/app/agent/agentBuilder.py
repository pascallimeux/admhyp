from config import ROOT_DIR
from app.common.log import get_logger
from app.common.lcmds import exec_local_cmd
from shutil import copyfile
from app.common.ssh import Ssh
logger = get_logger()

def update_agent(agent_name, broker_address):
    agent_properties_file_tmp = "{}/agent/properties/properties.tmp".format(ROOT_DIR)
    agent_properties_file     = "{}/agent/properties/properties.go".format(ROOT_DIR)
    copyfile(agent_properties_file_tmp, agent_properties_file)
    with open(agent_properties_file_tmp, "rt") as fin:
        with open(agent_properties_file, "wt") as fout:
            for line in fin:
                fout.write(line.replace('__BROKERADD__', broker_address).replace('__AGENTNAME__', agent_name))

def build_agent():
    exec_local_cmd("GOOS=linux && go build -ldflags='-s -w' -o {0}/agent/bin/hyp-agent {0}/agent/agent.go && upx -1 {0}/agent/bin/hyp-agent".format(ROOT_DIR))

def deploy_Agent(agent_name, password, hostname, login, broker_address, pub_key_file):
    update_agent(agent_name, broker_address)
    build_agent()
    ssh = Ssh(hostname=hostname, username=login, password=password)
    ssh.Upload_file("{0}/agent/bin/hyp-agent".format(ROOT_DIR), "/tmp/hyp-agent")
    with open(pub_key_file, 'r') as f:
        pubKey = f.read()
    cmd = "chmod u+x /tmp/hyp-agent && /tmp/hyp-agent -pubkey=\"{}\" -loglevel=debug -init=true".format(pubKey)
    ssh.exec_cmd(cmd, sudo=True)