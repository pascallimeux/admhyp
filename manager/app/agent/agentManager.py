from app.common.log import get_logger
from app.agent.message.messages import RESPONSETOPIC, ORDERTOPIC, STATUSTOPIC
from app.agent.message.messageHelper import build_sysinfo_dto, build_response_dto, create_order_dto
from app.node.services import NodeServices
from app.agent.message.messages import OrderType
from config import appconf
from app.agent.mqttHandler import MqttHandler
from app.common.lcmds import exec_local_cmd
from config import DEFAULTADMNAME, DEFAULTADMPWD

import abc, os, base64, time
logger = get_logger()

class Order():
    def __init__(self, id, agentId):
        self.messageId = id
        self.agentId = agentId

    def set_order(self, order_dto):
        self.sended = order_dto.created
        self.order = order_dto.order
        self.args = order_dto.args

    def set_response(self, response_dto):
        self.received = response_dto.created
        self.response = response_dto.response
        self.error = response_dto.error
        self.content = response_dto.content

    def to_str(self):
        return "MessageId={0}, AgentId={1}, Sended={2}, Received={3}, Order={4}, Response={5} ".format(self.messageId, self.agentId, self.sended, self.received, self.order, self.response)


class Observer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def receive_message(self, topic, message_dto):
        pass

class AgentManager(Observer):
    def __init__(self, agent_name=appconf().AGENTID, broker_add=appconf().BROKERIP, broker_port=appconf().BROKERPORT ):
        self.orders = {}
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
            order = Order(id, order_dto.agentId)
            order.set_order(order_dto)
            self.orders[id]=order
            logger.info("Order: {}".format(order.to_str()))

    def save_response(self, response_dto):
        id = response_dto.messageId
        if id not in self.orders:
            logger.error("No record orders for received response (messageId={})".format(id))
        else:
            order = self.orders['id']
            order.set_response(response_dto)

    def sub_agent(self, agent_name):
        topic = STATUSTOPIC + agent_name
        logger.info("Subscrite to {}".format(topic))
        self.comm_handler.Subscribe(topic)

    def stop_listener(self):
        self.comm_handler.StopHandler()

    def receive_message(self, topic, raw_message):
        if topic == STATUSTOPIC:
            sysinfo_dto = build_sysinfo_dto(raw_message)
            self.nodeService.update_info(sysinfo_dto)
            logger.info("Received system info from {}".format(sysinfo_dto.agentId))
        if topic == RESPONSETOPIC:
            response_dto = build_response_dto(raw_message)
            self.save_response(response_dto)
            logger.info("Received response: {0} from {1}".format(response_dto.order ,response_dto.AgentId))

    def exec_remote_cmd(self, agent_name, order, args=[]):
        order_dto = create_order_dto(order=order, args=args)
        order_id = order_dto.messageId
        order_json = order_dto.to_json()
        logger.info("Send message: {0} to agent: {1} ".format(str(order_dto.order), agent_name))
        self.save_order(order_dto)
        self.comm_handler.Publish(topic=ORDERTOPIC + agent_name, message_dto=order_json)
        return order_id

    def initenv(self, agent_name, remoteadmlogin=appconf().USERADM):
        orderid = self.exec_remote_cmd(agent_name=agent_name, order=OrderType.INITENV, args=[remoteadmlogin])
        start_time=time.time()
        while orderid not in self.orders and not timeout:
            delay = time.time()-start_time
            if delay > 10000:
                timeout = True
            print (delay)
            time.sleep(0.2)
        if not timeout:
            return self.order[orderid].response
        else:
            raise Exception("Timeout")

    def stop_agent(self, agent_name):
        self.exec_remote_cmd(agent_name=agent_name, order=OrderType.STOPAGENT)

    def deployca(self, agent_name):
        tgz_file = "/tmp/files.tgz"
        code = exec_local_cmd("cd {0}/data && tar czf {1} ./bin/fabric-ca-client "
                              "./bin/fabric-ca-server ./conf/config.yaml ./conf/fabric-ca-client-config.yaml".format(
            os.getcwd(), tgz_file))
        if code != 0:
            logger.error("Compress files for Ca failled!")
        else:
            with open(tgz_file, "rb") as f:
                encoded = base64.b64encode(f.read())
                encoded = str(encoded, 'utf-8')
            self.exec_remote_cmd(agent_name=agent_name, order=OrderType.DEPLOYCA,
                                 args=["/tmp/var/hyperledger/files.tgz", encoded])

    def startca(self, agent_name, hyp_adm_log=DEFAULTADMNAME, hyp_adm_pwd=DEFAULTADMPWD):
        self.exec_remote_cmd(agent_name=agent_name, order=OrderType.STARTCA, args=[hyp_adm_log, hyp_adm_pwd])

    def stopca(self, agent_name):
        self.exec_remote_cmd(agent_name=agent_name, order=OrderType.STOPCA, args=[])

    def iscastarted(self, agent_name):
        self.exec_remote_cmd(agent_name=agent_name, order=OrderType.ISCASTART, args=[])

    def iscadeployed(self, agent_name):
        self.exec_remote_cmd(agent_name=agent_name, order=OrderType.ISCADEPLOYED, args=[])



    def deploypeer(self, agent_name):
        tgz_file = "/tmp/files.tgz"
        code = exec_local_cmd ("cd {0}/data && tar czf {1} ./bin/peer ".format(os.getcwd(), tgz_file))
        if code != 0:
            logger.error("Compress files for Peer failled!")
        else:
            with open(tgz_file, "rb") as f:
                encoded = base64.b64encode(f.read())
                encoded = str(encoded,'utf-8')
            self.exec_remote_cmd(agent_name=agent_name, order=OrderType.DEPLOYPEER, args=["/tmp/var/hyperledger/files.tgz", encoded])

    def startpeer(self, agent_name, peer_name, peer_port="7051", mode="DEBUG"):
        self.exec_remote_cmd(agent_name=agent_name, order=OrderType.STARTPEER, args=[peer_name, mode, peer_port])

    def stoppeer(self, agent_name):
        self.exec_remote_cmd(agent_name=agent_name, order=OrderType.STOPPEER, args=[])

    def ispeerstarted(self, agent_name):
        self.exec_remote_cmd(agent_name=agent_name, order=OrderType.ISPEERSTART, args=[])

    def ispeerdeployed(self, agent_name):
        self.exec_remote_cmd(agent_name=agent_name, order=OrderType.ISPEERDEPLOYED, args=[])


    def deployorderer(self, agent_name):
        tgz_file = "/tmp/files.tgz"
        code = exec_local_cmd("cd {0}/data && tar czf {1} ./bin/orderer ".format(os.getcwd(), tgz_file))
        if code != 0:
            logger.error("Compress files for Orderer failled!")
        else:
            with open(tgz_file, "rb") as f:
                encoded = base64.b64encode(f.read())
                encoded = str(encoded, 'utf-8')
            self.exec_remote_cmd(agent_name=agent_name, order=OrderType.DEPLOYORDERER,
                                 args=["/tmp/var/hyperledger/files.tgz", encoded])

    def startoderer(self, agent_name):
        self.exec_remote_cmd(agent_name=agent_name, order=OrderType.STARTORDERER, args=[])

    def stoporderer(self, agent_name):
        self.exec_remote_cmd(agent_name=agent_name, order=OrderType.STOPORDERER, args=[])

    def isordererstarted(self, agent_name):
        self.exec_remote_cmd(agent_name=agent_name, order=OrderType.ISORDERERSTART, args=[])

    def isordererdeployed(self, agent_name):
        self.exec_remote_cmd(agent_name=agent_name, order=OrderType.ISORDERERDEPLOYED, args=[])



