from config import appconf, ROOT_DIR
from app.common.log import get_logger
from app.common.lcmds import exec_local_cmd
from app.agent.message.messages import RESPONSETOPIC, ORDERTOPIC, STATUSTOPIC, create_message
from shutil import copyfile
from app.common.ssh import Ssh
from config import appconf
from app.agent.mqttHandler import MqttHandler
import abc
logger = get_logger()

def Update_agent(agent_name, broker_address):
    agent_properties_file_tmp = "{}/agent/properties/properties.tmp".format(ROOT_DIR)
    agent_properties_file     = "{}/agent/properties/properties.go".format(ROOT_DIR)
    copyfile(agent_properties_file_tmp, agent_properties_file)
    with open(agent_properties_file_tmp, "rt") as fin:
        with open(agent_properties_file, "wt") as fout:
            for line in fin:
                fout.write(line.replace('__BROKERADD__', broker_address).replace('__AGENTNAME__', agent_name))

def Build_agent():
    exec_local_cmd("GOOS=linux && go build -ldflags='-s -w' -o {0}/agent/bin/hyp-agent {0}/agent/agent.go && upx -1 {0}/agent/bin/hyp-agent".format(ROOT_DIR))

def Deploy_Agent(agent_name, password, hostname, login=appconf().REMOTEUSERNAME, broker_address=appconf().BROKERADDRESS):
    Update_agent(agent_name, broker_address)
    Build_agent()
    ssh = Ssh(hostname=hostname, username=login, password=password)
    ssh.Upload_file("{0}/agent/bin/hyp-agent".format(ROOT_DIR), "/tmp/hyp-agent")
    with open(appconf().PUBKEYFILE, 'r') as f:
        pubKey = f.read()
    cmd = "chmod u+x /tmp/hyp-agent && /tmp/hyp-agent -pubkey=\"{}\" -loglevel=debug -init=true".format(pubKey)
    ssh.exec_cmd(cmd, sudo=True)

class Observer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add_message(self, message):
        pass

class AgentManager(Observer):
    def __init__(self, agent_name=appconf().AGENTID, broker_add=appconf().BROKERADDRESS, broker_port=appconf().BROKERPORT ):
        self.agents = []
        self.messages = []
        self.comm_handler = MqttHandler(agent_name=agent_name, broker_add=broker_add, broker_port=broker_port)
        self.comm_handler.Subscribe(RESPONSETOPIC + "#")

    def send_order(self, agent_name, mType, mBody):
        message = create_message(mtype=mType, body=mBody)
        self.comm_handler.Publish(topic=ORDERTOPIC + agent_name, message=message)

    def add_agent(self, agent_name):
        self.agents.append(agent_name)
        self.comm_handler.Subscribe(STATUSTOPIC + agent_name)

    def stop_communication(self):
        self.comm_handler.StopHandler()

    def add_message(self, message):
        self.message.append(message)