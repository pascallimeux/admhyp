import sys, os, time
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
import unittest
import threading
from app.common.services import ObjectNotFoundException
from app.agent.agentManager import AgentManager
from app.ca.services import CaServices
from app.peer.services import PeerServices
from app.orderer.services import OrdererServices
import  subprocess

from app.common.lcmds import exec_local_cmd

LOCALAGENT         = "127.0.0.1"
DEFAULTCANAME      = "ca1"
DEFAULTPEERNAME    = "peer1"
DEFAULTORDERERNAME = "orderer1"
DEFAULTPASSWORD    = "pascal"

class LocalAgent(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop = False
        self.cmd = "/opt/gopath/src/github.com/pascallimeux/admhyp/agent/bin/hyp-agent -name=\""+LOCALAGENT+"\""

    def run(self):
        process = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while not self.stop:
            nextline = process.stdout.readline()
            if nextline == '' and process.poll() is not None:
                break
            sys.stdout.write("AGENT "+LOCALAGENT+": > "+nextline.decode('utf-8'))
            sys.stdout.flush()
        output = process.communicate()[0]
        exitCode = process.returncode
        if (exitCode == 0):
            return output
        else:
            raise Exception(self.cmd, exitCode, output)

    def Stop(self):
        self.stop = True
        time.sleep(.5)
        cmd = "sudo kill -9 `pidof hyp-agent` 2>/dev/null"
        exec_local_cmd(cmd)



class mqttTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #cls.agent = LocalAgent()
        #cls.agent.start()
        try:
            caService = CaServices()
            caService.get_ca(name = DEFAULTCANAME)
        except ObjectNotFoundException:
            caService.create_ca(name=DEFAULTCANAME, hostname=LOCALAGENT, remotepassword=DEFAULTPASSWORD, deploy=False)
            print("create default ca")
        try:
            peerService = PeerServices()
            peerService.get_peer(name = DEFAULTPEERNAME)

        except ObjectNotFoundException:
            peerService.create_peer(name=DEFAULTPEERNAME, hostname=LOCALAGENT, remotepassword=DEFAULTPASSWORD, deploy=False)
            print("create default peer")
        try:
            ordererService = OrdererServices()
            ordererService.get_orderer(name = DEFAULTORDERERNAME)
        except ObjectNotFoundException:
            ordererService.create_orderer(name=DEFAULTORDERERNAME, hostname=LOCALAGENT, remotepassword=DEFAULTPASSWORD, deploy=False)
            print ("create default orderer")

    @classmethod
    def tearDownClass(cls):
        pass
        #cls.agent.Stop()

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
        response = self.agent_manager.iscastarted(agent_name=LOCALAGENT)
        self.assertTrue(response)

    def test_iscadeployed(self):
        response = self.agent_manager.iscadeployed(agent_name=LOCALAGENT)
        self.assertTrue(response)

    def test_stopca(self):
        response = self.agent_manager.stopca(agent_name=LOCALAGENT)
        self.assertTrue(response)
        response = self.agent_manager.iscastarted(agent_name=LOCALAGENT)
        self.assertFalse(response)


    def test_deploypeersynchrone(self):
        response = self.agent_manager.deploypeer(agent_name=LOCALAGENT)
        self.assertTrue(response)

    def test_start_agent(self):
        agent = LocalAgent()
        agent.start()
        time.sleep(3)
        agent.Stop()
