package mqtt

import (
	"encoding/json"
	"github.com/pascallimeux/admhyp/agent/logger"
	"math/rand"
	"time"
	"github.com/pascallimeux/admhyp/agent/syscommand"

)

type mtype int

const(
	SysInfoType	mtype = iota	// 0
	StopType			// 1
	ExecType			// 2
	UploadType			// 3
	AckType				// 4
	ErrorType			// 5
	ContentType			// 6
)


type Message struct {
	MessageId 	string
        AgentId 	string
        Created		time.Time
	Mtype           mtype
	Error	        string
	Body            string
	Tgz             []byte
}

func (m Message)ToJsonStr() string{
	json_mess, err := json.Marshal(m)
    	if err != nil {
		logger.Log.Error(err)
		return ""
    	}
	return string(json_mess)
}
func (m Message)ToStr() string{
	str := "AgentId="+m.AgentId
	str = str + " MessageId="+ m.MessageId
	str = str + " Created="+m.Created.String()
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

func GenerateAckMessage(agentName, messageID, content string) *Message {
	ack := &Message{MessageId:messageID, AgentId: agentName, Created: generateDate(), Mtype : AckType, Body:content}
	return ack
}

func GenerateErrorMessage(agentName, errorLabel, messageID string) *Message {
	if (messageID == ""){
		messageID = generateID(16)
	}
	error := &Message{MessageId:messageID, AgentId: agentName, Created: generateDate(), Mtype : ErrorType, Error:errorLabel}
	return error
}

func GenerateSysInfoMessage(agentName string) *Message {
	info, err := syscommand.GetSystemStatus()
	sysInfo := &Message{MessageId:generateID(16),  Mtype : SysInfoType, Created:generateDate()}
	if (err != nil){
		return GenerateErrorMessage(agentName, err.Error(), "")
	}
	sysInfo.Body=info.ToJsonStr()
	return sysInfo
}