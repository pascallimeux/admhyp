import paho.mqtt.client as mqtt
from threading import Thread
from app.agent.message.messages import build_message
from app.common.log import get_logger
logger = get_logger()



class MqttHandler(Thread):

    def __init__(self, agent_name, broker_add, broker_port, observer):
        Thread.__init__(self)
        self.observer = observer
        self.stop = False
        self.client = mqtt.Client(agent_name)
        self.client.on_connect = self.on_connect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_publish = self.on_publish
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        #self.client.on_log = self.on_log
        self.client.connect(broker_add, broker_port)
        self.start()

    def run(self):
        while not self.stop:
            self.client.loop()

    def StopHandler(self):
        self.stop = True

    def on_connect(self, mqttc, obj, flags, rc):
        logger.debug("rc: " + str(rc))

    def on_publish(self, mqttc, obj, mid):
        logger.debug("mid: " + str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        logger.debug("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_log(self, mqttc, obj, level, string):
        logger.debug("log: {}".format(string))

    def on_disconnect(self, mqttc, obj, rc):
        logger.debug("client disconnected ok")

    def Publish(self, topic, message):
        json_msg = message.to_json()
        self.client.publish(topic=topic, payload=json_msg, qos=1)

    def Subscribe(self, topic):
        self.client.subscribe(topic=topic)

    def on_message(self, mqttc, obj, msg):
        logger.debug(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        message = build_message(msg.topic, msg.payload)
        self.observer.add_message(message)