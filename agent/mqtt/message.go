package mqtt

import (
	"encoding/json"
	"github.com/pascallimeux/admhyp/agent/logger"
	"math/rand"
	"time"
	"github.com/pascallimeux/admhyp/agent/syscommand"

)

type orderType int

const(
       	STOPAGENT      orderType = iota // 0
       	DEPLOYCA			// 1
       	STARTCA                         // 2
      	ISCASTARTED                     // 3
       	ISCADEPLOYED			// 4
	STOPCA				// 5
	DEPLOYPEER                      // 6
       	STARTPEER                       // 7
       	ISPEERSTARTED                   // 8
       	ISPEERDEPLOYED			// 9
	STOPPEER			// 10
	DEPLOYORDERER                   // 11
       	STARTORDERER                    // 12
       	ISORDERERSTARTED                // 13
       	ISORDERERDEPLOYED		// 14
	STOPORDERER			// 15

)
type MessageDto struct {
	MessageId      string
        AgentId        string
        Created        time.Time
}

func ToJsonStr(obj interface{}) string{
       json_mess, err := json.Marshal(obj)
       if err != nil {
              logger.Log.Error(err)
              return ""
       }
       return string(json_mess)
}

func (m MessageDto)ToStr() string{
       str := "AgentId="+m.AgentId
       str = str + " MessageId="+ m.MessageId
       str = str + " Created="+m.Created.String()
       return str
}


type OrderDto struct {
       MessageId      string
       AgentId        string
       Created        time.Time
       Order          orderType
       Args           []string
}

func (o OrderDto)ToStr() string{
       str := "AgentId="+o.AgentId
       str = str + " MessageId="+ o.MessageId
       str = str + " Created="+o.Created.String()
       str = str + " Order="+o.Order
       return str
}

type ResponseDto struct {
       MessageId      string
       AgentId        string
       Created        time.Time
       Order          orderType
       Error          string
       Response       bool
       Content        []string
}


func (r ResponseDto)ToStr() string{
       str := "AgentId="+r.AgentId
       str = str + " MessageId="+ r.MessageId
       str = str + " Created="+r.Created.String()
       str = str + " Order="+r.Order
       str = str + " Order="+r.Response
       return str
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

func GenerateAckMessage(agentName, messageID, label string) *Message {
	content := []string{label}
	ack := &Message{MessageId:messageID, AgentId: agentName, Created: generateDate(), Mtype : AckType, Content:content}
	logger.Log.Debug("Send ack: "+ack.ToStr())
	return ack
}

func GenerateErrorMessage(agentName, errorLabel, messageID string) *Message {
	if (messageID == ""){
		messageID = generateID(16)
	}
	error := &Message{MessageId:messageID, AgentId: agentName, Created: generateDate(), Mtype : ErrorType, Error:errorLabel}
	logger.Log.Debug("Send error: "+error.ToStr())
	return error
}

func GenerateSysInfoMessage(agentName string) *Message {
	info, err := syscommand.GetSystemStatus()
	sysInfo := &Message{AgentId:agentName, MessageId:generateID(16),  Mtype : SysInfoType, Created:generateDate()}
	if (err != nil){
		return GenerateErrorMessage(agentName, err.Error(), "")
	}
	content := []string{info.ToJsonStr()}
	sysInfo.Content=content
	logger.Log.Debug("Send system info: "+sysInfo.ToStr())
	return sysInfo
}