from app.common.log import get_logger
from app.agent.message.messages import RESPONSETOPIC, ORDERTOPIC, STATUSTOPIC
from app.agent.message.messageHelper import build_sysinfo_dto, build_response_dto, create_order_dto
from app.node.services import NodeServices
from config import appconf
from app.agent.mqttHandler import MqttHandler
import abc
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


    #def upload_file(self, agent_name, source, dest):
    #    file_transfert = build_filetransfert(source, dest)
    #    self.send_order(agent_name=agent_name, mType=MessageType.DOWNLOAD, mContent=file_transfert.Content, filename = file_transfert.FileName)

    def exec_remote_cmd(self, agent_name, order, args):
        order_dto = create_order_dto(order=order, args=args)
        order_json = order_dto.to_json()
        logger.info("Send message: {0} to agent: {1} ".format(str(order_dto), agent_name))
        # logger.info("Send {0} message to agent: {1} ".format(mType, agent_name))
        self.save_order(order_dto)
        self.comm_handler.Publish(topic=ORDERTOPIC + agent_name, message_dto=order_json)





