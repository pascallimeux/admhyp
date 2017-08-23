import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from config import appconf
import unittest
from app.agent.agentBuilder import build_agent, deploy_Agent, update_agent

class AgentTest(unittest.TestCase):

    def test_Update_agent(self):
        update_agent(agent_name="127.0.0.1", broker_address=appconf().BROKERADDRESS)

    def test_Build_agent(self):
        build_agent()

    def test_Deploy_Agent(self):
        deploy_Agent(agent_name="127.0.0.1", password="pascal", hostname="127.0.0.1", login=appconf().REMOTEUSERNAME, broker_address=appconf().BROKERADDRESS, pub_key_file=appconf().PUBKEYFILE)

if __name__ == '__main__':
    unittest.main()