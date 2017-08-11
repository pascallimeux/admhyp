import paho.mqtt.client as mqtt
import time

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print("log: {}".format(string))


def on_disconnect(mqttc, obj, rc):
    print("client disconnected ok")



if __name__== '__main__':
    broker = "127.0.0.1"
    port = 1883

    client1 = mqtt.Client("agent1")
    client1.on_log = on_log
    client1.on_connect = on_connect
    client1.on_subscribe = on_subscribe
    client1.on_publish = on_publish
    client1.on_disconnect = on_disconnect
    client1.on_message = on_message
    client1.connect(broker, port)
    ret1 = client1.subscribe(topic="sensor/temperature",  qos=1)
    print("ret1={}".format(ret1))
    ret = client1.publish("sensor/temperature", 25.1, qos=1)
    print ("ret={}".format(ret))
    client1.loop_forever()
    #client1.disconnect()