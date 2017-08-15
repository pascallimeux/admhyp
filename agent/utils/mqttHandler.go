package utils

import ("container/list"
	MQTT "github.com/eclipse/paho.mqtt.golang"
	"time"
	"strconv"
)

type MqttHandler struct {
	BrokerAddress  string
	ClientID       string
	MqttClient     MQTT.Client
	topics         *list.List
	schedulesPubs  *list.List
}

func (m *MqttHandler) StopCommunication() error{
	m.stopSchedulePubs()
	err := m.unSubscribeTopics()
	if (err != nil){
		return err
	}
	m.MqttClient.Disconnect(250)
	log.Debug("Communication handler stopped...")
	return nil
}

func (m *MqttHandler) InitCommunication(fct func(string, []byte))error {
	log.Debug("Init communication for "+m.ClientID)
	var messageHandler MQTT.MessageHandler = func(client MQTT.Client, msg MQTT.Message) {
		fct(msg.Topic(), msg.Payload())
	}
	opts := MQTT.NewClientOptions().AddBroker(m.BrokerAddress)
	opts.SetClientID(m.ClientID)
	opts.SetDefaultPublishHandler(messageHandler)
	m.MqttClient = MQTT.NewClient(opts)
	if token := m.MqttClient.Connect(); token.Wait() && token.Error() != nil {
		log.Error(token.Error())
		return (token.Error())
	}
	m.topics = list.New()
	m.schedulesPubs = list.New()
	return nil
}

func (m *MqttHandler) SubscribeTopic(topicName string) error{
	log.Debug("subscribe topic:  "+topicName)
	m.topics.PushFront(topicName)
	if token := m.MqttClient.Subscribe(topicName, 0, nil); token.Wait() && token.Error() != nil {
		log.Error(token.Error())
		return token.Error()
	}
	return nil
}

func (m *MqttHandler) unSubscribeTopics() error {
	for e := m.topics.Front(); e != nil; e = e.Next() {
		if token := m.MqttClient.Unsubscribe(e.Value.(string)); token.Wait() && token.Error() != nil {
			log.Error(token.Error())
			return token.Error()
		}
		log.Debug("unsubscribe topic:  "+string(e.Value.(string)))
	}
	return nil
}

func (m *MqttHandler) PublishTopic(topicName, content string, ){
	log.Debug("publish on topic: "+topicName)
	token := m.MqttClient.Publish(topicName, 0, false, content)
	token.Wait()
}

func (m *MqttHandler) SchedulePub(fct func(), delay time.Duration){
	stopPub := Schedule(fct, delay)
	m.schedulesPubs.PushFront(stopPub)
}

func (m *MqttHandler) stopSchedulePubs() {
	log.Debug(strconv.Itoa(m.schedulesPubs.Len())+" schedule(s) publish topic(s) stopped...")
	for e := m.schedulesPubs.Front(); e != nil; e = e.Next() {
		e.Value.(chan bool) <- true
	}
}