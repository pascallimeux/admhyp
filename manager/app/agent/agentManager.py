from app.common.log import get_logger
from app.agent.message.messages import RESPONSETOPIC, ORDERTOPIC, STATUSTOPIC
from app.agent.message.messageHelper import build_sysinfo_dto, build_response_dto, create_order_dto
from app.node.services import NodeServices
from app.agent.message.messages import OrderType
from config import appconf
from app.agent.mqttHandler import MqttHandler
from app.common.lcmds import exec_local_cmd
from config import DEFAULTADMNAME, DEFAULTADMPWD
from config import MAXDELAYTORECEIVERESPONSE

import abc, os, base64, time
logger = get_logger()

class Message():
    def __init__(self, id, agentId, created):
        self.messageId = id
        self.agentId = agentId
        self.created = created

    def to_str(self):
        return "MessageId={0}, AgentId={1}, Created={2} ".format(self.messageId, self.agentId, self.created)

class Order(Message):
    def __init__(self, order_dto):
        super().__init__(order_dto.messageId, order_dto.agentId, order_dto.created)
        self.order = order_dto.order
        self.args = order_dto.args

    def to_str(self):
        str = super().to_str()
        str = str + " order:{0}".format(self.order)
        return str

class Response(Message):
    def __init__(self, response_dto):
        super().__init__(response_dto.messageId, response_dto.agentId, response_dto.created)
        self.order = response_dto.order
        self.response = response_dto.response
        self.error = response_dto.error
        self.content = response_dto.content

    def to_str(self):
        str = super().to_str()
        str = str + " order:{0} response:{1}".format(self.order, self.response)
        if self.error != "":
            str = str + " error:{}".format(self.error)
        return str

class Observer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def receive_message(self, topic, message_dto):
        pass

class AgentManager(Observer):
    def __init__(self, agent_name=appconf().AGENTID, broker_add=appconf().BROKERIP, broker_port=appconf().BROKERPORT ):
        self.orders = {}
        self.responses = {}
        self.nodeService = NodeServices()
        self.comm_handler = MqttHandler(agent_name=agent_name, broker_add=broker_add, broker_port=broker_port, observer=self)
        self.comm_handler.Subscribe(RESPONSETOPIC + "#")
        nodes = self.nodeService.get_nodes()
        for node in nodes:
            self.sub_agent(node.hostname)

    def save_order(self, order_dto):
        id = order_dto.messageId
        if id in self.orders:
            logger.error("Order already records (messageId={}".format(id))
        else:
            self.orders[id]=Order(order_dto)

    def save_response(self, response_dto):
        id = response_dto.messageId
        if id not in self.orders:
            logger.error("No records order for received response (messageId={})".format(id))
        else:
            self.responses[id]=Response(response_dto)
            logger.info("Order:    {}".format(self.orders[id].to_str()))
            logger.info("Response: {}".format(self.responses[id].to_str()))

    def sub_agent(self, agent_name):
        topic = STATUSTOPIC + agent_name
        logger.info("Subscrite to topic={}".format(topic))
        self.comm_handler.Subscribe(topic)

    def stop_listener(self):
        self.comm_handler.StopHandler()

    def start_listener(self):
        self.comm_handler.StartHandler()

    def receive_message(self, topic, raw_message):
        if STATUSTOPIC in topic:
            sysinfo_dto = build_sysinfo_dto(raw_message)
            self.nodeService.update_info(sysinfo_dto)
            logger.info("Received system info from {}".format(sysinfo_dto.agentId))
        if RESPONSETOPIC in topic:
            response_dto = build_response_dto(raw_message)
            self.save_response(response_dto)

    def exec_remote_cmd(self, agent_name, order, args=[], synchrone=False):
        order_dto = create_order_dto(order=order, args=args)
        order_id = order_dto.messageId
        order_json = order_dto.to_json()
        logger.info("Send message: {0} to agent: {1} ".format(str(order_dto.order), agent_name))
        self.save_order(order_dto)
        self.comm_handler.Publish(topic=ORDERTOPIC + agent_name, message_dto=order_json)
        if not synchrone:
            return order_id
        else:
            return self.wait_response(order_id)

    def wait_response(self, messageid):
        start_time = time.time()
        timeout = False
        while messageid not in self.responses and not timeout:
            delay = time.time() - start_time
            if delay > MAXDELAYTORECEIVERESPONSE:
                timeout = True
            time.sleep(0.1)
        if not timeout:
            logger.debug("receive response: " + str(self.responses[messageid].response))
            return self.responses[messageid].response
        else:
            logger.error("Timeout for order:{}".format(self.orders[messageid].to_str))
            return False


    def initenv(self, agent_name, remoteadmlogin=appconf().USERADM, synchrone=False):
        return self.exec_remote_cmd(agent_name=agent_name, order=OrderType.INITENV, args=[remoteadmlogin], synchrone=synchrone)


    def stop_agent(self, agent_name, synchrone=False):
        return self.exec_remote_cmd(agent_name=agent_name, order=OrderType.STOPAGENT, synchrone=synchrone)


    def deployca(self, agent_name, synchrone=False):
        tgz_file = "/tmp/files.tgz"
        code = exec_local_cmd("cd {0}/data && tar czf {1} ./bin/fabric-ca-client "
                              "./bin/fabric-ca-server ./conf/config.yaml ./conf/fabric-ca-client-config.yaml".format(
            os.getcwd(), tgz_file))
        if code != 0:
            logger.error("Compress files for Ca failled!")
            return False
        else:
            with open(tgz_file, "rb") as f:
                encoded = base64.b64encode(f.read())
                encoded = str(encoded, 'utf-8')
            return self.exec_remote_cmd(agent_name=agent_name, order=OrderType.DEPLOYCA,
                                 args=["/tmp/var/hyperledger/files.tgz", encoded], synchrone=synchrone)

    def startca(self, agent_name, hyp_adm_log=DEFAULTADMNAME, hyp_adm_pwd=DEFAULTADMPWD, synchrone=False):
        return self.exec_remote_cmd(agent_name=agent_name, order=OrderType.STARTCA, args=[hyp_adm_log, hyp_adm_pwd], synchrone=synchrone)

    def stopca(self, agent_name, synchrone=False):
        return self.exec_remote_cmd(agent_name=agent_name, order=OrderType.STOPCA, args=[], synchrone=synchrone)

    def iscastarted(self, agent_name, synchrone=False):
        return self.exec_remote_cmd(agent_name=agent_name, order=OrderType.ISCASTART, args=[], synchrone=synchrone)

    def iscadeployed(self, agent_name, synchrone=False):
        return self.exec_remote_cmd(agent_name=agent_name, order=OrderType.ISCADEPLOYED, args=[], synchrone=synchrone)



    def deploypeer(self, agent_name, synchrone=False):
        tgz_file = "/tmp/files.tgz"
        code = exec_local_cmd ("cd {0}/data && tar czf {1} ./bin/peer ".format(os.getcwd(), tgz_file))
        if code != 0:
            logger.error("Compress files for Peer failled!")
            return False
        else:
            with open(tgz_file, "rb") as f:
                encoded = base64.b64encode(f.read())
                encoded = str(encoded,'utf-8')
            return self.exec_remote_cmd(agent_name=agent_name, order=OrderType.DEPLOYPEER, args=["/tmp/var/hyperledger/files.tgz", encoded], synchrone=synchrone)

    def startpeer(self, agent_name, peer_name, peer_port="7051", mode="DEBUG", synchrone=False):
        return self.exec_remote_cmd(agent_name=agent_name, order=OrderType.STARTPEER, args=[peer_name, mode, peer_port], synchrone=synchrone)

    def stoppeer(self, agent_name, synchrone=False):
        return self.exec_remote_cmd(agent_name=agent_name, order=OrderType.STOPPEER, args=[], synchrone=synchrone)

    def ispeerstarted(self, agent_name, synchrone=False):
        return self.exec_remote_cmd(agent_name=agent_name, order=OrderType.ISPEERSTART, args=[], synchrone=synchrone)

    def ispeerdeployed(self, agent_name, synchrone=False):
        return self.exec_remote_cmd(agent_name=agent_name, order=OrderType.ISPEERDEPLOYED, args=[], synchrone=synchrone)


    def deployorderer(self, agent_name, synchrone=False):
        tgz_file = "/tmp/files.tgz"
        code = exec_local_cmd("cd {0}/data && tar czf {1} ./bin/orderer ".format(os.getcwd(), tgz_file))
        if code != 0:
            logger.error("Compress files for Orderer failled!")
            return False
        else:
            with open(tgz_file, "rb") as f:
                encoded = base64.b64encode(f.read())
                encoded = str(encoded, 'utf-8')
            return self.exec_remote_cmd(agent_name=agent_name, order=OrderType.DEPLOYORDERER,
                                 args=["/tmp/var/hyperledger/files.tgz", encoded], synchrone=synchrone)

    def startoderer(self, agent_name, synchrone=False):
        return self.exec_remote_cmd(agent_name=agent_name, order=OrderType.STARTORDERER, args=[], synchrone=synchrone)

    def stoporderer(self, agent_name, synchrone=False):
        return self.exec_remote_cmd(agent_name=agent_name, order=OrderType.STOPORDERER, args=[], synchrone=synchrone)

    def isordererstarted(self, agent_name, synchrone=False):
        return self.exec_remote_cmd(agent_name=agent_name, order=OrderType.ISORDERERSTART, args=[], synchrone=synchrone)

    def isordererdeployed(self, agent_name, synchrone=False):
        return self.exec_remote_cmd(agent_name=agent_name, order=OrderType.ISORDERERDEPLOYED, args=[], synchrone=synchrone)



