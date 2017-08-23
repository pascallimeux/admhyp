package main

import (
	"os"
	"time"
	"github.com/pascallimeux/admhyp/agent/mqtt"
	"github.com/pascallimeux/admhyp/agent/syscommand"
	"github.com/pascallimeux/admhyp/agent/properties"
	"flag"
	"github.com/pascallimeux/admhyp/agent/logger"
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
	logger.Log.Info("Agent "+a.AgentName+" initialization...")
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
	logger.Log.Info("Agent "+a.AgentName+" starting...")
	time.Sleep(5) // Required when the agent is starting at the system startup
	a.stopAgent = false

	err := a.commHandler.InitCommunication(a.processingOrders)
	if (err != nil){
		return err
	}

	err = a.commHandler.SubscribeTopic(properties.ORDERTOPIC+a.AgentName)
	if (err != nil){
		return err
	}

	//a.commHandler.SchedulePub(a.sendSystemStatus, properties.DELAYPUBSYSSTATUS)

	for !a.stopAgent {
		time.Sleep(properties.AGENTINACTIVATIONDELAY)
	}

	err = a.commHandler.StopCommunication()
	if (err != nil){
		return err
	}
	logger.Log.Info("Agent stopped...")
	return nil
}

func(a *Agent) sendSystemStatus(){
	sysInfoDto, err := mqtt.GenerateSysInfoMessage(a.AgentName)
	if (err == nil) {
		json_mess := mqtt.ToJsonStr(sysInfoDto)
		a.commHandler.PublishTopic(properties.STATUSTOPIC + a.AgentName, string(json_mess))
	}
}

func (a *Agent) processingOrders(topic string, bOrder []byte) {
	var responseDto *mqtt.ResponseDto
	var err error
	responseDto, a.stopAgent, err = mqtt.ProcessingOrders(bOrder)
	if (err == nil) {
		json_resp := mqtt.ToJsonStr(responseDto)
		a.commHandler.PublishTopic(properties.RESPONSETOPIC + responseDto.MessageId, json_resp)
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
	_, err := syscommand.CreateFile("/lib/systemd/system/"+a.ServiceName, serviceContent)
	if err != nil {
		logger.Log.Error(err)
		return err
	}
	cmd1 := "sudo systemctl enable "+serviceName
	cmd2 := "sudo systemctl start "+serviceName
	_, err = syscommand.ExecCmd(cmd1)
	if err != nil {
		logger.Log.Error(err)
		return err
	}
	_, err = syscommand.ExecCmd(cmd2)
	if err != nil {
		logger.Log.Error(err)
		return err
	}
	return nil
}

func (a *Agent) createAgentEnv(repo string) error{
	_, err := syscommand.CreateDirectory(repo)
	return err
}

func (a *Agent) createUser(username, publicKey string) error{
	_, err := syscommand.CreateAccount(username)
	if (err != nil){
		return err
	}
	err = syscommand.AddSudo(username)
	if (err != nil){
		return err
	}
	if publicKey != "None" {
		err = syscommand.AuthorizedKey(username, publicKey)
		if (err != nil){
			return err
		}
	}
	return nil
}

func (a *Agent) moveAgent(accountName, newpath, agentName string) error{
	agentPath, err := syscommand.GetProgrammFullName()
	agentPath = agentPath+"/"+agentName
	if err != nil {
		logger.Log.Error(err)
		return err
	}
	if (newpath == agentPath){
		logger.Log.Info("agent is already at the good place: " + agentPath)
		return nil
	}
	logger.Log.Info("Move agent from: " + agentPath + " to " + newpath)
	err = syscommand.MoveFile(agentPath, newpath)
	if err != nil {
		logger.Log.Error(err)
		return err
	}
	cmd0 := "sudo chown "+accountName+"."+accountName+" "+newpath
	_, err = syscommand.ExecCmd(cmd0)
	if err != nil {
		logger.Log.Error(err)
		return err
	}
	cmd1 := "sudo chmod 100 "+newpath
	_, err = syscommand.ExecCmd(cmd1)
	if err != nil {
		logger.Log.Error(err)
		return err
	}
	//return a.startNewAgent(accountName, newpath)
	return nil
}

func (a *Agent) startNewAgent(accountName, path string) error {
	logger.Log.Debug("startAgent(path:"+path+") : calling method -")
	err := syscommand.ExecDetachCmd(accountName, path)
	if err != nil {
		logger.Log.Error(err)
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
	logger.InitLog("agent", *logLevel)
	logger.Log.Info("Run Agent: {broker:"+*brokerAdd+", agentName:"+ *agentName+", AccountName:"+properties.ACCOUNTNAME+ " ,ServiceName:"+properties.SERVICENAME+" ,Repository:"+properties.REPOSITORY+"}")

	mqttHandler := mqtt.MqttHandler{ClientID:*agentName, BrokerAddress:*brokerAdd}
	agent := Agent{commHandler:mqttHandler, AccountName:properties.ACCOUNTNAME, AgentFileName:properties.AGENTFILENAME, ServiceName:properties.SERVICENAME, Repository:properties.REPOSITORY, AgentName:*agentName}
	if *init {
		agent.Init(*publicKey)
	}else {
		agent.Start()
	}
}