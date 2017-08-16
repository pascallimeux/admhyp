import paho.mqtt.client as mqtt
import json
from threading import Thread
from app.common.log import get_logger
logger = get_logger()

class Message ():
    def __init__(self, id, body, error):
        self.Id = id
        self.Body = body
        self.Error = error

    def __str__(self):
        return "Id={0}, Body={1}, Error={2}".format(self.Id, self.Body, self.Error)

    def To_json(self):
        return json.dumps(self)

def build_message(json_message):
    return json.loads(json_message)


class MqttHandler(Thread):

    def __init__(self, agent_name, broker_add, broker_port):
        Thread.__init__(self)
        self.start()
        self.agents =[]
        self.client = mqtt.Client(agent_name)
        self.client.on_connect = self.on_connect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_publish = self.on_publish
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.on_log = self.on_log
        self.client.connect(broker_add, broker_port)

    def run(self):
        while True:
            self.client.loop()

    def on_connect(self, mqttc, obj, flags, rc):
        logger.debug("rc: " + str(rc))


    def on_message(self, mqttc, obj, msg):
        logger.debug(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        message = build_message(msg.payload)
        logger.debug(message)


    def on_publish(self, mqttc, obj, mid):
        logger.debug("mid: " + str(mid))


    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        logger.debug("Subscribed: " + str(mid) + " " + str(granted_qos))


    def on_log(self, mqttc, obj, level, string):
        logger.debug("log: {}".format(string))


    def on_disconnect(self, mqttc, obj, rc):
        logger.debug("client disconnected ok")

    def Add_agent(self, agent_name):
        self.agents.append(agent_name)
        self.Subscribe("status/"+agent_name)

    def Publish(self, topic, message):
        self.client.publish(topic=topic, payload=message, qos=1)

    def Subscribe(self, topic):
        self.client.subscribe(topic=topic)

