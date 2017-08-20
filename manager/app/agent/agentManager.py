from app.common.log import get_logger
from app.agent.message.messages import RESPONSETOPIC, ORDERTOPIC, STATUSTOPIC, MessageType
from app.agent.message.messageBuilder import create_sended_message, build_received_message
from app.node.services import NodeServices
from config import appconf
from app.agent.mqttHandler import MqttHandler
import abc
logger = get_logger()


class Observer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def receive_message(self, topic, message_dto):
        pass

class AgentManager(Observer):
    def __init__(self, agent_name=appconf().AGENTID, broker_add=appconf().BROKERIP, broker_port=appconf().BROKERPORT ):
        self.messages = []
        self.nodeService = NodeServices()
        self.comm_handler = MqttHandler(agent_name=agent_name, broker_add=broker_add, broker_port=broker_port, observer=self)
        self.comm_handler.Subscribe(RESPONSETOPIC + "#")
        nodes = self.nodeService.get_nodes()
        for node in nodes:
            self.sub_agent(node.name)

    def sub_agent(self, agent_name):
        self.nodeService.get_node(agent_name)
        self.comm_handler.Subscribe(STATUSTOPIC + agent_name)

    def stop_listener(self):
        self.comm_handler.StopHandler()

    def send_message(self, agent_name, mType, mBody):
        message = create_sended_message(mtype=mType, body=mBody)
        message_dto = message.to_json()
        logger.info("Send message: {0} to agent: {1} ".format(str(message_dto), agent_name))
        self.comm_handler.Publish(topic=ORDERTOPIC + agent_name, message_dto=message_dto)

    def receive_message(self, topic, message_dto):
        message = build_received_message(topic, message_dto)
        if message.Mtype == MessageType.SYSINFO:
            self.nodeService.update_info(message)
        logger.info("Received message: {0} from agent:{1}".format(message.to_str() ,message.AgentId))
        self.messages.append(message)