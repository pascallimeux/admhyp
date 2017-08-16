package main

import (
	"os"
	"time"
	"github.com/pascallimeux/admhyp/agent/utils"
	"github.com/pascallimeux/admhyp/agent/mqtt"
	"github.com/pascallimeux/admhyp/agent/log"
	"github.com/pascallimeux/admhyp/agent/system"
	"github.com/pascallimeux/admhyp/agent/properties"
	"flag"
)

type Agent struct {
	AgentFileName  string
	AccountName    string
	ServiceName    string
	Repository     string
	AgentName      string
	stopAgent      bool
	commHandler    mqtt.MqttHandler
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
	err = a.moveAgent(a.AccountName, a.Repository+"/"+a.AgentFileName, a.AgentFileName)
	if err != nil {
		return err
	}
	err = a.persistAgent(a.ServiceName)
	if err != nil {
		return err
	}
	os.Exit(0)
	return nil
}


func(a *Agent) Start() error{
	log.Info("Agent starting...")
	time.Sleep(2) // Required when the agent is starting at the system startup
	a.stopAgent = false

	err := a.commHandler.InitCommunication(a.processingOrders)
	if (err != nil){
		return err
	}

	err = a.commHandler.SubscribeTopic(properties.ORDERTOPIC+a.AgentName)
	if (err != nil){
		return err
	}

	a.commHandler.SchedulePub(a.sendSystemStatus, properties.DELAYPUBSYSSTATUS)

	for !a.stopAgent {
		time.Sleep(properties.AGENTINACTIVATIONDELAY)
	}

	err = a.commHandler.StopCommunication()
	if (err != nil){
		return err
	}
	log.Info("Agent stopped...")
	return nil
}

func(a *Agent) sendSystemStatus(){
	message := system.GetSystemStatus()
	json_mess := message.ToJsonStr()
	a.commHandler.PublishTopic(properties.STATUSTOPIC+a.AgentName, string(json_mess))
}

func (a *Agent) processingOrders(topic string, bMessage []byte) {
	response := mqtt.ProcessingOrders(topic, bMessage)
	json_resp := response.ToJsonStr()
	a.commHandler.PublishTopic(properties.RESPONSETOPIC + a.AgentName + "/" + response.Id, json_resp)
	if (response.Body == "Agent stopped..."){
		a.stopAgent = true
	}
}

func (a *Agent) persistAgent(serviceName string) error{
	serviceContent := "[Unit]\n"
	serviceContent = serviceContent + "Description=agent for hyperledger supervision\n"
	serviceContent = serviceContent + "After=network.target\n"
	serviceContent = serviceContent + "Requires=network.target\n"
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
	cmd1 := "sudo systemctl enable "+serviceName
	cmd2 := "sudo systemctl start "+serviceName
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

func (a *Agent) moveAgent(accountName, newpath, agentName string) error{
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


func main() {
	var brokerAdd = flag.String("broker", properties.DEFAULTBROKERADD, "broker address" )
	var logLevel = flag.String("loglevel", properties.DEFAULTLOGLEVEL, "level for log")
	var agentName = flag.String("name", properties.DEFAULTAGENTNAME, "name of the agent")
	var publicKey = flag.String("pubkey", "None", "admin ssh public key" )
	var init = flag.Bool("init", false, "initialize agent" )
	flag.Parse()
	log.InitLog("agent", *logLevel)
	log.Info("Run Agent: {broker:"+*brokerAdd+", agentName:"+ *agentName+", AccountName:"+properties.ACCOUNTNAME+ " ,ServiceName:"+properties.SERVICENAME+" ,Repository:"+properties.REPOSITORY+"}")

	mqttHandler := mqtt.MqttHandler{ClientID:*agentName, BrokerAddress:*brokerAdd}
	agent := Agent{commHandler:mqttHandler, AccountName:properties.ACCOUNTNAME, AgentFileName:properties.AGENTFILENAME, ServiceName:properties.SERVICENAME, Repository:properties.REPOSITORY, AgentName:*agentName}
	if *init {
		agent.Init(*publicKey)
	}else {
		agent.Start()
	}
}