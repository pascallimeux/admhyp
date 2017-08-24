package mqtt

import (
	"encoding/json"
	"time"

	"github.com/pascallimeux/admhyp/agent/syscommand"
	"github.com/pascallimeux/admhyp/agent/logger"
	"strconv"
	"github.com/pascallimeux/admhyp/agent/properties"
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
	INITENV				// 16

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

func (m *MessageDto)ToStr() string{
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

func (o *OrderDto)ToStr() string{
       str := "AgentId="+o.AgentId
       str = str + " MessageId="+ o.MessageId
       str = str + " Created="+o.Created.String()
       str = str + " Order="+string(o.Order)
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


func (r *ResponseDto)ToStr() string{
       str := "AgentId="+r.AgentId
       str = str + " MessageId="+ r.MessageId
       str = str + " Created="+r.Created.String()
       str = str + " Order="+string(r.Order)
       str = str + " Order="+strconv.FormatBool(r.Response)
       return str
}

type SysInfoDto struct {
	MessageId      		string
        AgentId        		string
        Created        		time.Time
        TotalMemory		float64
        FreeMemory      	float64
        UsedMemory      	float64
        TotalDisk       	float64
        FreeDisk        	float64
        UsedDisk		float64
        CpusUtilisation 	[]float64
        Ca_deployed     	bool
        Ca_started		bool
        Orderer_deployed	bool
        Orderer_started		bool
        Peer_deployed		bool
        Peer_started		bool
}

func (s *SysInfoDto)ToStr() string{
        str := "AgentId="+s.AgentId
        str = str + " MessageId="+ s.MessageId
        str = str + " Created="+s.Created.String()
        return str
}

func (s *SysInfoDto)SetInfo(info syscommand.SysInfo){
	s.TotalMemory=info.TotalMemory
	s.FreeMemory=info.FreeMemory
        s.UsedMemory=info.UsedMemory
        s.TotalDisk=info.TotalDisk
        s.FreeDisk=info.FreeDisk
        s.UsedDisk=info.UsedDisk
        s.CpusUtilisation=info.CpusUtilisation
	s.Ca_deployed=IsDeployed(properties.CABINARYNAME)
        s.Ca_started=IsStarted(properties.CAPROCESSNAME)
        s.Orderer_deployed=IsDeployed(properties.ORDERERBINARYNAME)
        s.Orderer_started=IsStarted(properties.ORDERERPROCESSNAME)
        s.Peer_deployed=IsDeployed(properties.PEERBINARYNAME)
        s.Peer_started=IsStarted(properties.PEERPROCESSNAME)
}


