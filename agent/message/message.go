package message

import (
	"encoding/json"
	"github.com/pascallimeux/admhyp/agent/utils"
)

var log = utils.GetLogger()

type Message struct {
	Id   string
	Body string
}

func (m Message)ToJsonStr() (string, error){
	json_mess, err := json.Marshal(m)
    	if err != nil {
		log.Error(err)
		return "", err
    	}
	return string(json_mess), nil
}
