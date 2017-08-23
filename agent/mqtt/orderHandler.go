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
	logger.Log.Debug(string(bOrder))
	err := json.Unmarshal(bOrder, &order_dto)
	if (err != nil) {
		logger.Log.Error(err)
		return nil, false, err
	}
	response_dto := &ResponseDto{MessageId:order_dto.MessageId, AgentId:order_dto.AgentId, Created:generateDate(), Order:order_dto.Order }

	order := order_dto.Order
	switch order{
	case STOPAGENT:
		StopAgent(response_dto)
		stopAgent=true

	case DEPLOYCA:
		DeployCa(response_dto)

	case STARTCA:
		StartCa(response_dto, order_dto.Args)

	case ISCASTARTED:
		IsStarted(response_dto, properties.CAPROCESSNAME)

	case ISCADEPLOYED:
		IsDeployed(response_dto, properties.CABINARYNAME)

	case STOPCA:
		StopProcess(response_dto, properties.CAPROCESSNAME)

	case DEPLOYPEER:
		DeployPeer(response_dto)

	case STARTPEER:
		StartPeer(response_dto, order_dto.Args)

	case ISPEERSTARTED:
		IsStarted(response_dto, properties.PEERPROCESSNAME)

	case ISPEERDEPLOYED:
		IsDeployed(response_dto, properties.PEERBINARYNAME)

	case STOPPEER:
		StopProcess(response_dto, properties.PEERPROCESSNAME)

	case DEPLOYORDERER:
		DeployOrderer(response_dto)

	case STARTORDERER:
		StartOrderer(response_dto)

	case ISORDERERSTARTED:
		IsStarted(response_dto, properties.ORDERERPROCESSNAME)

	case ISORDERERDEPLOYED:
		IsDeployed(response_dto, properties.ORDERERBINARYNAME)

	case STOPORDERER:
		StopProcess(response_dto, properties.ORDERERPROCESSNAME)

	case UPLOADINFOSYS:

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
	logger.Log.Debug(response)
	response_dto.Response = true
	response_dto.Error = error
}

func StartCa(response_dto *ResponseDto, params []string) {
	if len(params) != 2 {
		response_dto.Error = "Bad arguments number for method StartCa(" + (strings.Join(params, ","))+")"
	}
	admin_name := params[0]
	admin_pwd := params[1]
	cmd := "cd /var/hyperledger && CMD=\"./bin/fabric-ca-server start -b " + admin_name + ":'" + admin_pwd + "' -c .keys/config.yaml > log/ca.log 2>&1 &\" && eval \"$CMD\""
	exec_local_cmd(response_dto, cmd)
}

func StartPeer(response_dto *ResponseDto, params []string) {
	if len(params) != 3 {
		response_dto.Error = "Bad arguments number for method StartPeer(" + (strings.Join(params, ","))+")"
	}
	peer_name := params[0]
	mode := params[1]
	peer_port :=params[2]
	cmd := "FABRIC_CFG_PATH=$PWD CORE_PEER_ID=" + peer_name + " CORE_PEER_ADDRESSAUTODETECT=true CORE_PEER_ADDRESS=" + peer_name + ":" + peer_port +
		"CORE_PEER_GOSSIP_EXTERNALENDPOINT=" + peer_name + ":" + peer_port + " CORE_PEER_GOSSIP_ORGLEADER=false CORE_PEER_GOSSIP_USELEADERELECTION=true "+
		"CORE_PEER_GOSSIP_SKIPHANDSHAKE=true CORE_PEER_MSPCONFIGPATH=/var/hyperledger/msp CORE_PEER_LOCALMSPID=BlockChainCoCMSP CORE_LOGGING_LEVEL=" + mode +
		" /var/hyperledger/bin/peer node start"
	exec_local_cmd(response_dto, cmd)
}

func StartOrderer(response_dto *ResponseDto) {
	cmd := "/var/hyperledger/bin/orderer"
	exec_local_cmd(response_dto, cmd)
}

func DeployCa(response_dto *ResponseDto){

}

func DeployPeer(response_dto *ResponseDto){

}

func DeployOrderer(response_dto *ResponseDto){

}

func StopProcess(response_dto *ResponseDto, process_name string) {
	cmd := "kill -9 `pidof "+process_name+"` 2>/dev/null"
	exec_local_cmd(response_dto, cmd)
}

func IsStarted(response_dto *ResponseDto, process_name string) (string, string){
	cmd := "PID=`pidof "+process_name+"` && [ -n \"$PID\" ] && echo True || echo False"
	return syscommand.ExecComplexCmd(cmd)
}

func IsDeployed(response_dto *ResponseDto, binaryName string) (string, string){
	cmd :="if [ -f "+binaryName+" ] ; then echo \"True\" ; else echo \"False\" ; fi"
	return syscommand.ExecComplexCmd(cmd)
}


func Download(fileName, content string)(string, error){
	logger.Log.Debug("Write file: "+ fileName)
	decoded := make([]byte, b64.StdEncoding.DecodedLen(len(content)))
	if _, err := b64.StdEncoding.Decode(decoded, []byte(content)); err != nil {
		return "",err
	}
	if err := ioutil.WriteFile(fileName, decoded, 0644); err != nil {
		return "",err
	}
	if err := syscommand.Uncompress(fileName, "/tmp/var/hyperledger"); err != nil {
		return "",err
	}
	return fileName + " upload on agent", nil
}


func GenerateSysInfoMessage(agentName string) (*SysInfoDto, error) {
	info, err := syscommand.GetSystemStatus()
	sysInfoDto := &SysInfoDto{AgentId:agentName, MessageId:generateID(16), Created:generateDate()}
	if (err != nil){
		logger.Log.Error(err)
	}
	sysInfoDto.SetInfo(info)
	logger.Log.Debug("Send system info: "+sysInfoDto.ToStr())
	return sysInfoDto, err
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
