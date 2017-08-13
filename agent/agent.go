package main

import (
	"fmt"
	MQTT "github.com/eclipse/paho.mqtt.golang"
	"os"
	"time"
	"github.com/pascallimeux/admhyp/agent/utils"
	"flag"
	"github.com/op/go-logging"
)

var log *logging.Logger

const (
	AGENTFILENAME = "hyp-agent"
	REPOSITORY    = "/var/hyperledger"
	ACCOUNTNAME   = "orangeadm"
	SERVICENAME   = "hyp-agent.service"
)

type Agent struct {
	BrokerAddress  string
	AgentFileName  string
	AccountName    string
	ServiceName    string
	Repository     string
	AgentName      string
	MqttClient     MQTT.Client
}

func(a *Agent) Init(publicKey string) error{
	log.Info("Agent initialization...")
	err := a.createUser(a.AccountName, publicKey)
	if err != nil {
		return err
	}
	err = a.createAgentEnv(a.Repository)
	if err != nil {
		return err
	}
	err = a.Move(a.AccountName, a.Repository+"/"+a.AgentFileName, a.AgentFileName)
	if err != nil {
		return err
	}
	err = a.PersistAgent(a.ServiceName)
	if err != nil {
		return err
	}
	os.Exit(0)
	return nil
}

func(a *Agent) Start() error{
	log.Info("Agent starting...")
	opts := MQTT.NewClientOptions().AddBroker(a.BrokerAddress)
	opts.SetClientID(a.AgentName)
	opts.SetDefaultPublishHandler(messageHandler)

	a.MqttClient = MQTT.NewClient(opts)
	if token := a.MqttClient.Connect(); token.Wait() && token.Error() != nil {
		return (token.Error())
	}

	if token := a.MqttClient.Subscribe(a.AgentName+"/sample", 0, nil); token.Wait() && token.Error() != nil {
		fmt.Println(token.Error())
		os.Exit(1)
	}

	for i := 0; i < 5; i++ {
		text := fmt.Sprintf("this is msg #%d!", i)
		token := a.MqttClient.Publish(a.AgentName+"/sample", 0, false, text)
		token.Wait()
	}

	time.Sleep(3 * time.Second)

	if token := a.MqttClient.Unsubscribe(a.AgentName+"/sample"); token.Wait() && token.Error() != nil {
		fmt.Println(token.Error())
		os.Exit(1)
	}

	a.MqttClient.Disconnect(250)
	return nil
}

func (a *Agent) PersistAgent(serviceName string) error{
	serviceContent := "[Unit]\n"
	serviceContent = serviceContent + "Description=agent for hyperledger supervision\n"
	serviceContent = serviceContent + "After=tlp-init.service\n\n"
	serviceContent = serviceContent + "[Service]\n"
	serviceContent = serviceContent + "User="+a.AccountName+"\n"
	serviceContent = serviceContent + "ExecStart="+a.Repository+"/"+a.AgentFileName+"\n\n"
	serviceContent = serviceContent + "[Install]\n"
	serviceContent = serviceContent + "WantedBy=multi-user.target\n"
	_, err := utils.CreateFile("/lib/systemd/system/"+a.ServiceName, serviceContent)
	if err != nil {
		log.Error(err)
		return err
	}
	cmd1 := "sudo chmod a+x /lib/systemd/system/"+serviceName
	cmd2 := "sudo systemctl enable "+serviceName
	cmd3 := "sudo systemctl start "+serviceName
	_, err = utils.ExecCmd(cmd1)
	if err != nil {
		log.Error(err)
		return err
	}
	_, err = utils.ExecCmd(cmd2)
	if err != nil {
		log.Error(err)
		return err
	}
	_, err = utils.ExecCmd(cmd3)
	if err != nil {
		log.Error(err)
		return err
	}
	return nil
}


func (a *Agent) createAgentEnv(repo string) error{
	_, err := utils.CreateDirectory(repo)
	return err
}

func (a *Agent) createUser(username, publicKey string) error{
	_, err := utils.CreateAccount(username)
	if (err != nil){
		return err
	}
	err = utils.AddSudo(username)
	if (err != nil){
		return err
	}
	if publicKey != "None" {
		err = utils.AuthorizedKey(username, publicKey)
		if (err != nil){
			return err
		}
	}
	return nil
}

func (a *Agent) Move(accountName, newpath, agentName string) error{
	agentPath, err := utils.GetProgrammFullName()
	agentPath = agentPath+"/"+agentName
	if err != nil {
		log.Error(err)
		return err
	}
	if (newpath == agentPath){
		log.Info("agent is already at the good place: " + agentPath)
		return nil
	}
	log.Info("Move agent from: " + agentPath + " to " + newpath)
	err = utils.MoveFile(agentPath, newpath)
	if err != nil {
		log.Error(err)
		return err
	}
	cmd0 := "sudo chown "+accountName+"."+accountName+" "+newpath
	_, err = utils.ExecCmd(cmd0)
	if err != nil {
		log.Error(err)
		return err
	}
	cmd1 := "sudo chmod 100 "+newpath
	_, err = utils.ExecCmd(cmd1)
	if err != nil {
		log.Error(err)
		return err
	}
	//return a.startNewAgent(accountName, newpath)
	return nil
}

func (a *Agent) startNewAgent(accountName, path string) error {
	log.Debug("startAgent(path:"+path+") : calling method -")
	err := utils.ExecDetachCmd(accountName, path)
	if err != nil {
		log.Error(err)
		return err
	}
	os.Exit(0)
	return nil
}


var messageHandler MQTT.MessageHandler = func(client MQTT.Client, msg MQTT.Message) {
	fmt.Printf("TOPIC: %s\n", msg.Topic())
	fmt.Printf("MSG: %s\n", msg.Payload())
}

func main() {
	var brokerAdd = flag.String("broker", "tcp://127.0.0.1:1883", "broker address" )
	var publicKey = flag.String("pubkey", "None", "admin ssh public key" )
	var init = flag.Bool("init", false, "initialize agent" )
	var logLevel = flag.String("loglevel", "debug", "level for log")
	var agentName = flag.String("name", "agentX", "name of the agent")
	flag.Parse()
	log = utils.InitLog("agent", *logLevel)
	log.Info("Init Agent: {broker:"+*brokerAdd+", agentName:"+ *agentName+", AccountName:"+ACCOUNTNAME+ " ,ServiceName:"+SERVICENAME+" ,Repository:"+REPOSITORY+"}")
	agent := Agent{BrokerAddress:*brokerAdd, AccountName:ACCOUNTNAME, AgentFileName:AGENTFILENAME, ServiceName:SERVICENAME, Repository:REPOSITORY, AgentName:*agentName}
	if *init {
		agent.Init(*publicKey)
	}else {
		agent.Start()
	}
}