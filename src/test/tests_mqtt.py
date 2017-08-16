import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
import unittest
from app.agent.MqttHandler import MqttHandler

class mqttTest(unittest.TestCase):

    def test_1(self):
        handler = MqttHandler(agent_name="manager", broker_add="127.0.0.1", broker_port=1883)
        handler.Add_agent("agentA")
        while (True):
            pass

