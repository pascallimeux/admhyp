package mqtt

import (
	"encoding/json"
	"github.com/pascallimeux/admhyp/agent/logger"
)

func ProcessingOrders(topic, agentName string, bMessage []byte) *Message {
	message := &Message{}
	responseContent := ""
	err := json.Unmarshal(bMessage, &message)
	if (err != nil) {
		logger.Log.Error(err)
		error := GenerateErrorMessage(agentName, "Bad message format!", "")
		return error
	}
	logger.Log.Debug("Process message: " + message.ToStr()+ " on topic: "+topic)
	switch message.Mtype{
	case StopType:
		responseContent = "Agent stopped..."
	case ExecType:
		responseContent = "Agent execute action..."
	case UploadType:
		responseContent = "Agent upload file..."

	default:
		return GenerateErrorMessage(agentName, "Unknown action requested!", message.MessageId)
	}
	response := GenerateAckMessage(agentName, message.MessageId, responseContent)
	return response
}



