package main

import (
"fmt"
//import the Paho Go MQTT library
MQTT "github.com/eclipse/paho.mqtt.golang"
"os"
"time"
	"github.com/op/go-logging"

	"github.com/pascallimeux/admhyp/agent/utils"

)
var log = logging.MustGetLogger("agent")

type Agent struct {
	BrokerAddress   string
}

func(a *Agent) Init(){
	//utils.Create_directory("/var/hyperledger")
	//a.MoveAndRestart("/var/hyperledger/agent")
	//a.PersistAgent()
	utils.Create_admin_account("orangeadm", "kkkkkkk")
}

func (a *Agent) PersistAgent(){
	utils.Is_service_active("agent_hyp.service")
}

func (a *Agent) MoveAndRestart(newpath string) error{
	agentPath, err := utils.GetProgrammFullName()
	if err != nil {
		return err
	}
	if (newpath == agentPath){
		log.Debug("agent is arleady at the good place: " + agentPath)
		return nil
	}
	log.Debug("Move agent from: " + agentPath + " to " + newpath)
	err = utils.MoveFile(agentPath, newpath)
	if err != nil {
		return err
	}
	return a.startNewAgent(newpath)
}

func (a *Agent) startNewAgent(path string) error {
	log.Debug("startAgent(path:"+path+") : calling method -")
	err := utils.Exec_detach_cmd(path)
	if err != nil {
		return err
	}
	os.Exit(0)
	return nil
}


//define a function for the default message handler
var f MQTT.MessageHandler = func(client MQTT.Client, msg MQTT.Message) {
	fmt.Printf("TOPIC: %s\n", msg.Topic())
	fmt.Printf("MSG: %s\n", msg.Payload())
}





func main() {
	agent := Agent{
		BrokerAddress:            "tcp://127.0.0.1:1883",
	}
	agent.Init()
}

func main2() {
	//create a ClientOptions struct setting the broker address, clientid, turn
	//off trace output and set the default message handler
	opts := MQTT.NewClientOptions().AddBroker("tcp://127.0.0.1:1883")
	opts.SetClientID("agent2")
	opts.SetDefaultPublishHandler(f)

	//create and start a client using the above ClientOptions
	c := MQTT.NewClient(opts)
	if token := c.Connect(); token.Wait() && token.Error() != nil {
		panic(token.Error())
	}

	//subscribe to the topic /go-mqtt/sample and request messages to be delivered
	//at a maximum qos of zero, wait for the receipt to confirm the subscription
	if token := c.Subscribe("go-mqtt/sample", 0, nil); token.Wait() && token.Error() != nil {
		fmt.Println(token.Error())
		os.Exit(1)
	}

	//Publish 5 messages to /go-mqtt/sample at qos 1 and wait for the receipt
	//from the server after sending each message
	for i := 0; i < 5; i++ {
		text := fmt.Sprintf("this is msg #%d!", i)
		token := c.Publish("go-mqtt/sample", 0, false, text)
		token.Wait()
	}

	time.Sleep(3 * time.Second)

	//unsubscribe from /go-mqtt/sample
	if token := c.Unsubscribe("go-mqtt/sample"); token.Wait() && token.Error() != nil {
		fmt.Println(token.Error())
		os.Exit(1)
	}

	c.Disconnect(250)
}