package properties

import "time"

const (
	AGENTFILENAME          = "hyp-agent"
	REPOSITORY             = "/tmp/var/hyperledger"
	REPOBIN		       = REPOSITORY+"/bin"
	REPOCONF	       = REPOSITORY+"/conf"
	ACCOUNTNAME            = "orangeadm"
	SERVICENAME            = "hyp-agent.service"
	STATUSTOPIC            = "status/"	// status/clientID
	ORDERTOPIC             = "orders/"	// orders/clientID
	RESPONSETOPIC          = "responses/"   // responses/clientID/messageID
	DEFAULTLOGLEVEL        = "debug"
	DELAYPUBSYSSTATUS      = 10 *time.Second
	AGENTINACTIVATIONDELAY = 500 * time.Millisecond
	DEFAULTBROKERADD       = "tcp://127.0.0.1:1883"
	DEFAULTAGENTNAME       = "127.0.0.1"
	PEERPROCESSNAME        = "peer"
	CAPROCESSNAME          = "fabric-ca-server"
	ORDERERPROCESSNAME     = "orderer"
	PEERBINARYNAME         = "peer"
	CABINARYNAME           = "fabric-ca-server"
	ORDERERBINARYNAME      = "orderer"
)
