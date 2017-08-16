import paho.mqtt.client as mqtt
import time

class MqttHandler():

    def InitCommunication(self, agent_name):
        self.client = mqtt.Client(agent_name)
        self.client.on_connect = self.on_connect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_publish = self.on_publish
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

    def on_connect(self, mqttc, obj, flags, rc):
        print("rc: " + str(rc))


    def on_message(self, mqttc, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


    def on_publish(self, mqttc, obj, mid):
        print("mid: " + str(mid))


    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))


    def on_log(self, mqttc, obj, level, string):
        print("log: {}".format(string))


    def on_disconnect(self, mqttc, obj, rc):
        print("client disconnected ok")



if __name__== '__main__':
    broker = "127.0.0.1"
    port = 1883

    client1 = mqtt.Client("manager")
    client1.on_log = on_log
    client1.on_connect = on_connect
    client1.on_subscribe = on_subscribe
    client1.on_publish = on_publish
    client1.on_disconnect = on_disconnect
    client1.on_message = on_message
    client1.connect(broker, port)
    ret1 = client1.subscribe(topic="status/#")
    print("ret1={}".format(ret1))
    #ret = client1.publish("sensor/temperature", 25.1, qos=1)
    #print ("ret={}".format(ret))
    client1.loop_forever()
    #client1.disconnect()