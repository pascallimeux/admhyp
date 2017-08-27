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
	REMOVEENV			// 17
	REGISTERUSER			// 18
	REGISTERNODE			// 19
	REGISTERADMIN			// 20
	ENROLLUSER			// 21
	ENROLLNODE			// 22
	ENROLLADMIN			// 23
)

type MessageDto struct {
	MessageId      string		`json:"messageid"`
        AgentId        string		`json:"agentid"`
        Created        time.Time	`json:"created"`
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
	MessageId      string		`json:"messageid"`
        AgentId        string		`json:"agentid"`
        Created        time.Time	`json:"created"`
	Order          orderType	`json:"order"`
        Args           []string		`json:"args,omitempty"`
}

func (o *OrderDto)ToStr() string{
       str := "AgentId="+o.AgentId
       str = str + " MessageId="+ o.MessageId
       str = str + " Created="+o.Created.String()
       str = str + " Order="+string(o.Order)
       return str
}

type ResponseDto struct {
	MessageId      string		`json:"messageid"`
        AgentId        string		`json:"agentid"`
        Created        time.Time	`json:"created"`
        Order          orderType	`json:"order"`
        Error          string		`json:"data,omitempty"`
        Response       bool		`json:"response"`
        Content        []string		`json:"data,omitempty"`
}


func (r *ResponseDto)ToStr() string{
       str := "AgentId="+r.AgentId
       str = str + " MessageId="+ r.MessageId
       str = str + " Created="+r.Created.String()
       str = str + " Order="+string(r.Order)
       str = str + " Response="+strconv.FormatBool(r.Response)
       return str
}

type SysInfoDto struct {
	MessageId      		string		`json:"messageid"`
        AgentId        		string		`json:"agentid"`
        Created        		time.Time	`json:"created"`
        TotalMemory		float64		`json:"totalmemory"`
        FreeMemory      	float64		`json:"freememory"`
        UsedMemory      	float64		`json:"usedmemory"`
        TotalDisk       	float64		`json:"totaldisk"`
        FreeDisk        	float64		`json:"freedisk"`
        UsedDisk		float64		`json:"useddisk"`
        CpusUtilisation 	[]float64	`json:"cpusutilisation"`
        Ca_deployed     	bool		`json:"cadeployed"`
        Ca_started		bool		`json:"castarted"`
        Orderer_deployed	bool		`json:"ordererdeployed"`
        Orderer_started		bool		`json:"ordererstarted"`
        Peer_deployed		bool		`json:"peerdeployed"`
        Peer_started		bool		`json:"peerstarted"`
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


