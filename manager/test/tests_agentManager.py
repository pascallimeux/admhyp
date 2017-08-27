import sys, os, time
import unittest
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from app.login.services import UserServices
from app.agent.agentManager import AgentManager
from app.ca.services import CaServices
from app.peer.services import PeerServices
from app.orderer.services import OrdererServices
from app.common.lcmds import Threading_cmd
from config import appconf

LOCALAGENT         = "127.0.0.1"
DEFAULTCANAME      = "ca1"
DEFAULTPEERNAME    = "peer1"
DEFAULTORDERERNAME = "orderer1"
DEFAULTPASSWORD    = "pascal"

ADMIN1NAME = "adm1"
USER1NAME  = "user1"
NODE1NAME  = "node1"
ADMIN1PWD  = "adm1pwd"
USER1PWD   = "user1pwd"
NODE1PWD   = "node1pwd"

class mqttTest(unittest.TestCase):



    @classmethod
    def setUpClass(cls):
        cls.init_DB()
        #cls.start_local_agent()
        caService = CaServices()
        caService.create_ca(name=DEFAULTCANAME, hostname=LOCALAGENT, remotepassword=DEFAULTPASSWORD, deploy=False)
        peerService = PeerServices()
        peerService.create_peer(name=DEFAULTPEERNAME, hostname=LOCALAGENT, remotepassword=DEFAULTPASSWORD, deploy=False)
        ordererService = OrdererServices()
        ordererService.create_orderer(name=DEFAULTORDERERNAME, hostname=LOCALAGENT, remotepassword=DEFAULTPASSWORD, deploy=False)

    @classmethod
    def tearDownClass(cls):
        pass
        #cls.agent.Stop()

    @classmethod
    def init_DB(cls):
        cls.userServices = UserServices()
        cls.userServices.DropDB()
        cls.userServices.CreateDB()

    @classmethod
    def start_local_agent(cls):
        cmd = "/opt/gopath/src/github.com/pascallimeux/admhyp/agent/bin/hyp-agent -name=\"" + LOCALAGENT + "\""
        cls.agent = Threading_cmd(cmd=cmd, processname="hyp-agent", username=appconf().USERADM)
        cls.agent.start()

    def setUp(self):
        self.agent_manager = AgentManager()

    def tearDown(self):
        self.agent_manager.stop_listener()

    def test_stopagentsynchrone(self):
        response = self.agent_manager.stop_agent(agent_name=LOCALAGENT, synchrone=True)
        self.assertTrue(response)

    def test_initenvsynchrone(self):
        start = time.time()
        response = self.agent_manager.initenv(agent_name=LOCALAGENT, synchrone=True)
        stop = time.time()
        print ("execution time: " + str(stop-start))
        self.assertTrue(response)

    def test_ca(self):
        response = self.agent_manager.removeenv(agent_name=LOCALAGENT, synchrone=True)
        self.assertTrue(response)

        response = self.agent_manager.initenv(agent_name=LOCALAGENT, synchrone=True)
        self.assertTrue(response)

        response = self.agent_manager.iscadeployed(agent_name=LOCALAGENT, synchrone=True)
        self.assertFalse(response)

        response = self.agent_manager.iscastarted(agent_name=LOCALAGENT, synchrone=True)
        self.assertFalse(response)

        response = self.agent_manager.deployca(agent_name=LOCALAGENT, synchrone=True)
        self.assertTrue(response)

        response = self.agent_manager.iscadeployed(agent_name=LOCALAGENT, synchrone=True)
        self.assertTrue(response)

        response = self.agent_manager.iscastarted(agent_name=LOCALAGENT, synchrone=True)
        self.assertFalse(response)

        response = self.agent_manager.startca(agent_name=LOCALAGENT, synchrone=True)
        self.assertTrue(response)

        response = self.agent_manager.iscastarted(agent_name=LOCALAGENT, synchrone=True)
        self.assertTrue(response)

        response = self.agent_manager.stopca(agent_name=LOCALAGENT, synchrone=True)
        self.assertTrue(response)

        response = self.agent_manager.iscastarted(agent_name=LOCALAGENT, synchrone=True)
        self.assertFalse(response)

        response = self.agent_manager.removeenv(agent_name=LOCALAGENT, synchrone=True)
        self.assertTrue(response)

        response = self.agent_manager.iscadeployed(agent_name=LOCALAGENT, synchrone=True)
        self.assertFalse(response)


    def __test_initenv(self):
        self.agent_manager.initenv(agent_name=LOCALAGENT)
        time.sleep(1)

    def test_deploy_casynchrone(self):
        response = self.agent_manager.deployca(agent_name=LOCALAGENT, synchrone=True)
        self.assertTrue(response)

    def test_start_casynchrone(self):
        response = self.agent_manager.startca(agent_name=LOCALAGENT, synchrone=True)
        self.assertTrue(response)

    def test_iscastartedsynchrone(self):
        response = self.agent_manager.iscastarted(agent_name=LOCALAGENT, synchrone=True)
        self.assertTrue(response)

    def test_iscadeployed(self):
        response = self.agent_manager.iscadeployed(agent_name=LOCALAGENT, synchrone=True)
        self.assertTrue(response)

    def test_stopca(self):
        response = self.agent_manager.stopca(agent_name=LOCALAGENT, synchrone=True)
        self.assertTrue(response)

    def test_sysinfo(self):
        time.sleep(12)


    def test_deploypeersynchrone(self):
        response = self.agent_manager.deploypeer(agent_name=LOCALAGENT, synchrone=True)
        self.assertTrue(response)


    def test_register_admin(self):
        response = self.agent_manager.initenv(agent_name=LOCALAGENT, synchrone=True)
        self.assertTrue(response)

        response = self.agent_manager.deployca(agent_name=LOCALAGENT, synchrone=True)
        self.assertTrue(response)

        response = self.agent_manager.startca(agent_name=LOCALAGENT, synchrone=True)
        self.assertTrue(response)

        response = self.agent_manager.register_admin(agent_name=LOCALAGENT, adm_name=ADMIN1NAME, adm_pwd=ADMIN1PWD, synchrone=True)

    def test_register_user(self):
        response = self.agent_manager.register_user(agent_name=LOCALAGENT, username=USER1NAME, pwd=USER1PWD, synchrone=True)

    def test_register_node(self):
        response = self.agent_manager.regiDEFAULTPASSWORDster_node(agent_name=LOCALAGENT,nodename=NODE1NAME, nodepwd=NODE1PWD , synchrone=True)

    def enroll_admin(self):
        response = self.agent_manager.enroll_admin(agent_name=LOCALAGENT, adm_name=ADMIN1NAME, adm_pwd=ADMIN1PWD, synchrone=True)

    def enroll_user(self):
        response = self.agent_manager.renroll_user(agent_name=LOCALAGENT, username=USER1NAME, pwd=USER1PWD, synchrone=True)

    def enroll_node(self):
        response = self.agent_manager.enroll_node(agent_name=LOCALAGENT, nodename=NODE1NAME, nodepwd=NODE1PWD, synchrone=True)