package mqtt

import (
	"encoding/json"
	"github.com/pascallimeux/admhyp/agent/logger"
	"github.com/pascallimeux/admhyp/agent/properties"
	"github.com/pascallimeux/admhyp/agent/syscommand"
	//"compress/zlib"
	b64 "encoding/base64"
	//"io/ioutil"
	"io/ioutil"
	"strings"
	"time"
	"math/rand"
)

func ProcessingOrders(bOrder []byte) (*ResponseDto, bool, error) {
	order_dto := &OrderDto{}
	stopAgent :=false
	err := json.Unmarshal(bOrder, &order_dto)
	if (err != nil) {
		logger.Log.Error(err)
		return nil, false, err
	}
	response_dto := &ResponseDto{MessageId:order_dto.MessageId, AgentId:order_dto.AgentId, Created:generateDate(), Order:order_dto.Order }
	order := order_dto.Order
	logger.Log.Debug("receive order: "+string (int(order)))
	switch order{
	case INITENV:
		BuildHyperledgerFolders(response_dto, order_dto.Args)

	case STOPAGENT:
		StopAgent(response_dto)
		stopAgent=true

	case DEPLOYCA:
		Deploy(response_dto, order_dto.Args)

	case STARTCA:
		StartCa(response_dto, order_dto.Args)

	case ISCASTARTED:
		response_dto.Response = IsStarted(properties.CAPROCESSNAME)

	case ISCADEPLOYED:
		response_dto.Response = IsDeployed(properties.CABINARYNAME)

	case STOPCA:
		StopProcess(response_dto, properties.CAPROCESSNAME)

	case DEPLOYPEER:
		Deploy(response_dto, order_dto.Args)

	case STARTPEER:
		StartPeer(response_dto, order_dto.Args)

	case ISPEERSTARTED:
		response_dto.Response = IsStarted(properties.PEERPROCESSNAME)

	case ISPEERDEPLOYED:
		response_dto.Response  = IsDeployed(properties.PEERBINARYNAME)

	case STOPPEER:
		StopProcess(response_dto, properties.PEERPROCESSNAME)

	case DEPLOYORDERER:
		Deploy(response_dto, order_dto.Args)

	case STARTORDERER:
		StartOrderer(response_dto)

	case ISORDERERSTARTED:
		response_dto.Response = IsStarted(properties.ORDERERPROCESSNAME)

	case ISORDERERDEPLOYED:
		response_dto.Response = IsDeployed(properties.ORDERERBINARYNAME)

	case STOPORDERER:
		StopProcess(response_dto, properties.ORDERERPROCESSNAME)

	case REMOVEENV:
		RemoveHyperledgerFolders(response_dto)

	case REGISTERUSER:
		RegisterUser(response_dto, order_dto.Args)

	case REGISTERNODE:
		RegisterNode(response_dto, order_dto.Args)

	case REGISTERADMIN:
		RegisterAdmin(response_dto, order_dto.Args)

	case ENROLLUSER:
		EnrollUser(response_dto, order_dto.Args)

	case ENROLLNODE:
		EnrollNode(response_dto, order_dto.Args)

	case ENROLLADMIN:
		EnrollAdmin(response_dto, order_dto.Args)

	default:
		UnknownMethod(response_dto, order)
	}
	return response_dto, stopAgent, nil
}


func UnknownMethod (response_dto *ResponseDto, order orderType){
	response_dto.Response = false
	response_dto.Error = "Unknown action requested "+ string(order)
}

func StopAgent(response_dto *ResponseDto){
	response := true
	response_dto.Response = response
}

func exec_local_cmd(response_dto *ResponseDto, cmd string) {
	response, error := syscommand.ExecComplexCmd(cmd)
	response_dto.Error = error
	if (error != "" && response != ""){
		response_dto.Response = false
	}else{
		response_dto.Response = true
	}
}

func RemoveHyperledgerFolders(response_dto *ResponseDto){
	cmd := "sudo rm -R "+properties.REPOSITORY
	exec_local_cmd(response_dto, cmd)
}

func BuildHyperledgerFolders(response_dto *ResponseDto, params []string) {
	username := params[0]
	group := params[0]
	cmd := "sudo mkdir -p "+properties.REPOSITORY+"/.keys/admin " +
	 "&& sudo mkdir -p "+properties.REPOSITORY+"/log " +
         "&& sudo chown -R "+username+"."+group+" "+properties.REPOSITORY +
         "&& sudo mkdir -p /opt/gopath/src/github.com/hyperledger " +
         "&& sudo chown "+username+"."+group+" /opt/gopath/src/github.com/hyperledger "
	exec_local_cmd(response_dto, cmd)
}

func StartCa(response_dto *ResponseDto, params []string) {
	if len(params) != 2 {
		response_dto.Error = "Bad arguments number for method StartCa(" + (strings.Join(params, ","))+")"
	}else {
		admin_name := params[0]
		admin_pwd := params[1]
		cmd := "cd " + properties.REPOSITORY + " && CMD=\"./bin/fabric-ca-server start -b " + admin_name + ":'" + admin_pwd + "' -c .keys/config.yaml > log/ca.log 2>&1 &\" && eval \"$CMD\""
		exec_local_cmd(response_dto, cmd)
	}
}

func StartPeer(response_dto *ResponseDto, params []string) {
	if len(params) != 3 {
		response_dto.Error = "Bad arguments number for method StartPeer(" + (strings.Join(params, ","))+")"
	}else {
		peerName := params[0]
		mode := params[1]
		peerPort := params[2]
		cmd := "FABRIC_CFG_PATH=$PWD CORE_PEER_ID=" + peerName + " CORE_PEER_ADDRESSAUTODETECT=true CORE_PEER_ADDRESS=" + peerName + ":" + peerPort +
			"CORE_PEER_GOSSIP_EXTERNALENDPOINT=" + peerName + ":" + peerPort + " CORE_PEER_GOSSIP_ORGLEADER=false CORE_PEER_GOSSIP_USELEADERELECTION=true " +
			"CORE_PEER_GOSSIP_SKIPHANDSHAKE=true CORE_PEER_MSPCONFIGPATH=" + properties.REPOSITORY + "/msp CORE_PEER_LOCALMSPID=BlockChainCoCMSP CORE_LOGGING_LEVEL=" + mode +
			" " + properties.REPOBIN + "/peer node start"
		exec_local_cmd(response_dto, cmd)
	}
}

func StartOrderer(response_dto *ResponseDto) {
	cmd := properties.REPOBIN+"/orderer"
	exec_local_cmd(response_dto, cmd)
}


func Deploy(response_dto *ResponseDto, params []string){
	if len(params) != 2 {
		response_dto.Error = "Bad arguments number for method Deploy(" + (strings.Join(params, ","))+")"
	}else {
		tgzFile := params[0]
		encoded := params[1]
		decoded := make([]byte, b64.StdEncoding.DecodedLen(len(encoded)))
		if _, err := b64.StdEncoding.Decode(decoded, []byte(encoded)); err != nil {
			response_dto.Error = err.Error()
			return
		}
		if err := ioutil.WriteFile(tgzFile, decoded, 0644); err != nil {
			response_dto.Error = err.Error()
			return
		}
		cmd := "cd " + properties.REPOSITORY + " && tar xzf " + tgzFile + " . && rm " + tgzFile
		exec_local_cmd(response_dto, cmd)
	}
}

func StopProcess(response_dto *ResponseDto, process_name string) {
	cmd := "kill -9 `pidof "+process_name+"` 2>/dev/null"
	exec_local_cmd(response_dto, cmd)
}

func IsStarted(process_name string) bool{
	cmd := "PID=`pidof "+process_name+"` && [ -n \"$PID\" ] && echo \"True\" || echo \"False\""
	response, _ := syscommand.ExecComplexCmd(cmd)
	logger.Log.Debug("RESPONSE:"+response+")")
	if (strings.Contains(response, "True")){
		return true
	}
	if (response == "False"){
		logger.Log.Debug("444")
		return false
	}
	return false
}

func IsDeployed(binaryName string) bool{
	cmd :="if [ -f "+properties.REPOBIN+"/"+binaryName+" ] ; then echo \"True\" ; else echo \"False\" ; fi"
	resp, err := syscommand.ExecComplexCmd(cmd)
	if (err != "") || (strings.Contains(resp ,"False")){
		return false
	}
	return true
}

func GenerateSysInfoMessage(agentName string) (*SysInfoDto, error) {
	info, err := syscommand.GetSystemStatus()
	sysInfoDto := &SysInfoDto{AgentId:agentName, MessageId:generateID(16), Created:generateDate()}
	if (err != nil){
		logger.Log.Error(err)
	}
	sysInfoDto.SetInfo(info)
	logger.Log.Debug("Send system info: "+ToJsonStr(sysInfoDto))
	return sysInfoDto, err
}

func RegisterAdmin(response_dto *ResponseDto, params []string) {
	if len(params) != 2 {
		response_dto.Error = "Bad arguments number for method Register admin(" + (strings.Join(params, ","))+")"
	}else {
		admName := params[0]
		admPwd  := params[1]
		register(response_dto, admName, admPwd, "client")
	}
}


func RegisterUser(response_dto *ResponseDto, params []string) {
	if len(params) != 2 {
		response_dto.Error = "Bad arguments number for method Register user(" + (strings.Join(params, ","))+")"
	}else {
		userName := params[0]
		userPwd  := params[1]
		register(response_dto, userName, userPwd, "user")
	}
}


func RegisterNode(response_dto *ResponseDto, params []string) {
	if len(params) != 2 {
		response_dto.Error = "Bad arguments number for method Register node(" + (strings.Join(params, ","))+")"
	}else {
		nodeName := params[0]
		nodePwd  := params[1]
		register(response_dto, nodeName, nodePwd, "peer")
	}
}

func register(response_dto *ResponseDto, idname, idpwd, idtype string){
	isCaStarted := IsStarted(properties.CAPROCESSNAME)
	if !isCaStarted {
		response_dto.Error = "Register failled, Ca is not started!"
	}else {
		cmd := "cd " + properties.REPOSITORY + " && ./bin/fabric-ca-client register --id.name " + idname + " --id.type " + idtype + " --id.affiliation org1.department1 --id.secret " + idpwd
		exec_local_cmd(response_dto, cmd)
	}
}

func enroll(name, password, repo string) string{
	cmd := " ./bin/fabric-ca-client enroll -u http://" + name + ":'" + password + "'@localhost:7054 -c " + properties.REPOSITORY + "/.keys/"+repo+"/fabric-ca-client-config.yaml "
      	return cmd
}

func EnrollAdmin(response_dto *ResponseDto, params []string) {
	if len(params) != 3 {
		response_dto.Error = "Bad arguments number for method Enroll admin(" + (strings.Join(params, ","))+")"
	}else {

		adminName := params[0]
		adminPwd  := params[1]
		login     := params[2]
		cmd :="cd " + properties.REPOSITORY + enroll(adminName, adminPwd, "admin") +
		"&& sudo mkdir -p /home/"+login+"/.fabric-ca-client " +
		"&& sudo cp -R " + properties.REPOSITORY +"/.keys/admin/* /home/"+login+"/.fabric-ca-client"
		exec_local_cmd(response_dto, cmd)
	}
}


func EnrollUser(response_dto *ResponseDto, params []string) {
	if len(params) != 2 {
		response_dto.Error = "Bad arguments number for method Enroll user(" + (strings.Join(params, ","))+")"
	}else {
		username := params[0]
		password := params[1]
		cmd := "mkdir -p " + properties.REPOSITORY +"/.msp/"+username +
		"&& cp " + properties.REPOSITORY + "/conf/fabric-ca-client-config.yaml " + properties.REPOSITORY + "/.msp/{0} " +
		"&& cd " + properties.REPOSITORY + enroll(username, password, username)
		exec_local_cmd(response_dto, cmd)
	}
}

func EnrollNode(response_dto *ResponseDto, params []string) {
	if len(params) != 2 {
		response_dto.Error = "Bad arguments number for method Enroll node(" + (strings.Join(params, ","))+")"
	}else {
		username := params[0]
		password := params[1]
		cmd := "mkdir -p " + properties.REPOSITORY + "/.keys/"+ username +
		"&& cp " + properties.REPOSITORY + "/conf/fabric-ca-client-config.yaml " + properties.REPOSITORY + "/.keys/{0} " +
		"&& cd " + properties.REPOSITORY + enroll(username, password, username)
		exec_local_cmd(response_dto, cmd)
	}
}

func generateID(n int) string{
	var letters = []rune("0123345678ABCDEF")
	b := make([]rune, n)
	for i := range b {
		b[i] = letters[rand.Intn(len(letters))]
	}
    return string(b)
}

func generateDate() time.Time {
	return time.Now()
}
