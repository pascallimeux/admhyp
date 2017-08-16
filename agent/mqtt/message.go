package mqtt

import (
	"encoding/json"
	"github.com/pascallimeux/admhyp/agent/log"
	"math/rand"
)

type Message struct {
	Id    string
	Body  string
	Error string
}

func (m Message)ToJsonStr() string{
	json_mess, err := json.Marshal(m)
    	if err != nil {
		log.Error(err)
		return ""
    	}
	return string(json_mess)
}

func GenerateID(n int) string{
	var letters = []rune("0123345678ABCDEF")
	b := make([]rune, n)
	for i := range b {
		b[i] = letters[rand.Intn(len(letters))]
	}
    return string(b)
}