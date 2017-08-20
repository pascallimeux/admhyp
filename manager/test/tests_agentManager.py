import sys, os, time
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
import unittest
from app.agent.agentManager import AgentManager
from app.agent.message.messages import MessageType
from app.node.model import Node
from app.ca.services import CaServices
from app.node.services import NodeServices
class mqttTest(unittest.TestCase):

    def test_1(self):
        agent_name = "agent"
        caService = CaServices()
        #caService.create_ca(name=agent_name, hostname="127.0.0.1", remotepassword="pascal")
        agent_manager = AgentManager()
        agent_manager.send_message(agent_name=agent_name, mType=MessageType.EXEC, mBody="Hello Agent....")
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
        service=CaServices()
        service.create_ca(name="agent1", hostname="127.0.0.1", remotepassword="pascal", deploy=False)
        service.create_ca(name="agent2", hostname="127.0.0.1", remotepassword="pascal", deploy=False)
        service.create_ca(name="agent3", hostname="127.0.0.1", remotepassword="pascal", deploy=False)
        service.create_ca(name="agent4", hostname="127.0.0.1", remotepassword="pascal", deploy=False)
        service.create_ca(name="agent5", hostname="127.0.0.1", remotepassword="pascal", deploy=False)
        ca1 = service.get_ca(name="agent1")
        service.create_ca

