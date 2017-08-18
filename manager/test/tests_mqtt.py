import sys, os, time, datetime
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
import unittest
from app.agent.agentManager import AgentManager
from app.agent.message.messages import MessageType
class mqttTest(unittest.TestCase):

    def test_1(self):
        agent_name = "agent1"
        agent_manager = AgentManager()
        agent_manager.add_agent(agent_name)
        agent_manager.send_order(agent_name=agent_name, mType=MessageType.exec, mBody="Hello Agent....")
        time.sleep(20)
        agent_manager.send_order(agent_name=agent_name, mType=MessageType.stop, mBody="Hello Agent....")
        time.sleep(60)
        agent_manager.stop_communication()


