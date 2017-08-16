import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
import unittest
from app.agent.agentManager import Build_agent, Deploy_Agent, Update_agent

class AgentTest(unittest.TestCase):

    def test_Update_agent(self):
        agent_name = "AGENT_A"
        broker_address = "tcp://127.0.0.1:1883"
        Update_agent(agent_name, broker_address)

    def test_Build_agent(self):
        Build_agent()

    def test_Deploy_Agent(self):
        Deploy_Agent(agent_name="agentA", password="pascal", hostname="192.168.0.103")

if __name__ == '__main__':
    unittest.main()