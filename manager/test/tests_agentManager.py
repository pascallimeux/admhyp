import sys, os, time
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
import unittest
from app.agent.agentManager import AgentManager
from app.node.model import Node
from app.ca.services import CaServices
from app.node.services import NodeServices
from app.peer.services import PeerServices
from app.orderer.services import OrdererServices
from app.agent.message.messages import OrderType
import base64
from app.common.lcmds import exec_local_cmd

class mqttTest(unittest.TestCase):

    def test_1(self):
        agent_name = "127.0.0.1"
        caService = CaServices()
        #caService.create_ca(name=agent_name, hostname="127.0.0.1", remotepassword="pascal")
        agent_manager = AgentManager()
        agent_manager.send_message(agent_name=agent_name, mType=MessageType.EXEC, mContent=['method', 'arg1', 'arg2', 'arg3'])
        time.sleep(20)
        agent_manager.send_message(agent_name=agent_name, mType=MessageType.STOP, mBody="Hello Agent....")
        time.sleep(5)
        #agent_manager.stop_listener()
        while True :
            pass
        for message in agent_manager.messages:
            print(message)

    def test_2(self):
        service = NodeServices()
        node = service.get_record(model=Node, name="agent5")
        print(node)

    def test_3(self):
        caService=CaServices()
        peerService = PeerServices()
        ordererService = OrdererServices()
        ordererService.create_orderer(name="orderer1", hostname="127.0.0.1", remotepassword="pascal", deploy=False)
        caService.create_ca(name="ca1", hostname="127.0.0.1", remotepassword="pascal", deploy=False)
        peerService.create_peer(name="peer1", hostname="127.0.0.1", remotepassword="pascal", deploy=False)

    def test_deploy_ca(self):
        caService = CaServices()
        caService.deploy_ca(name="ca1")


    def test_start_ca(self):
        caService = CaServices()
        caService.start_ca(name="ca1")


    def test_4(self):
        agent_name = "127.0.0.1"
        agent_manager = AgentManager()
        agent_manager.exec_remote_cmd(agent_name=agent_name, order=OrderType.STARTCA, args=['orangeadm', 'password'])
        #agent_manager.send_message(agent_name=agent_name, mType=MessageType.EXEC, mContent=['isstarted', 'hyp-agent'], filename="")

    def test_stopagent(self):
        agent_name = "127.0.0.1"
        agent_manager = AgentManager()
        agent_manager.stop_agent(agent_name=agent_name)

    def test_deployca(self):
        agent_name = "127.0.0.1"
        agent_manager = AgentManager()
        agent_manager.deployca(agent_name=agent_name)
        agent_manager.stop_listener()

    def test_iscastarted(self):
        agent_name = "127.0.0.1"
        agent_manager = AgentManager()
        agent_manager.iscastarted(agent_name=agent_name)
        time.sleep(5)
        agent_manager.stop_listener()

    def test_iscadeployed(self):
        agent_name = "127.0.0.1"
        agent_manager = AgentManager()
        agent_manager.iscadeployed(agent_name=agent_name)
        time.sleep(5)
        agent_manager.stop_listener()

    def test_stopca(self):
        agent_name = "127.0.0.1"
        agent_manager = AgentManager()
        agent_manager.stopca(agent_name=agent_name)
        time.sleep(10)
        agent_manager.stop_listener()

    def test_deploypeer(self):
        agent_name = "127.0.0.1"
        agent_manager = AgentManager()
        agent_manager.deploypeer(agent_name=agent_name)
        agent_manager.stop_listener()

    def test_deployorderer(self):
        agent_name = "127.0.0.1"
        agent_manager = AgentManager()
        agent_manager.deployorderer(agent_name=agent_name)
        agent_manager.stop_listener()

    def test_getsysinfo(self):
        agent_name = "127.0.0.1"
        caService = CaServices()
        caService.create_ca(name="ca6", hostname=agent_name, remotepassword="pascal", deploy=False)
        agent_manager = AgentManager()
        time.sleep(20)
        agent_manager.stop_listener()
