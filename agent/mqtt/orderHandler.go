package mqtt

import (
	"encoding/json"
	"github.com/pascallimeux/admhyp/agent/log"
)

func ProcessingOrders(topic string, bMessage []byte) Message {
	message := Message{}
	responseContent := ""
	err := json.Unmarshal(bMessage, &message)
	if (err != nil) {
		log.Error(err)
		response := Message{Id:GenerateID(16), Error:"Bad format!"}
		return response
	}
	log.Debug("TOPIC: " + topic + "\n")
	log.Debug("MSG  : " + message.Body + "\n")
	log.Debug("ERROR: " + message.Error + "\n")
	if (message.Body == "stop") {
		responseContent = "Agent stopped..."
	}else{
		// execute order
		responseContent = "Good response..."
	}
	response := Message{Id:message.Id, Body:responseContent}
	return response
}



