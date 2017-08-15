package message

import (
	"encoding/json"
)

func ProcessingOrders(topic string, bMessage []byte) Message {
	message := Message{}
	responseContent := ""
	err := json.Unmarshal(bMessage, &message)
	if (err != nil) {
		log.Error(err.Error())
		response := Message{Id:"FFFFFFFFFFFFFFFF", Body:"Bad format!"}
		return response
	}
	log.Debug("TOPIC: " + topic + "\n")
	log.Debug("MSG: " + message.Body + "\n")
	if (message.Body == "stop") {
		responseContent = "Agent stopped..."
	}else{
		// execute order
		responseContent = "Good response..."
	}
	response := Message{Id:message.Id, Body:responseContent}
	return response
}



