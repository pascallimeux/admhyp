package mqtt

import (
	"time"
	"testing"
	"os"
	"github.com/pascallimeux/admhyp/agent/properties"
	"github.com/pascallimeux/admhyp/agent/logger"
	"github.com/pascallimeux/admhyp/agent/syscommand"
)
const(
	USERNAME = "orangeadm"
	PASSWORD="orangeadm"
)


func setup() {
	var logLevel = properties.DEFAULTLOGLEVEL
	logger.InitLog("agent", logLevel)
}

func shutdown(){

}

func TestMain(m *testing.M) {
	setup()
	time.Sleep(time.Millisecond * 3000)
	code := m.Run()
	shutdown()
	os.Exit(code)
}


func TestIsStarted(t *testing.T) {
	response := IsStarted(properties.CAPROCESSNAME)
	if response {
		print(properties.CAPROCESSNAME + " is started")
	}else{
		print(properties.CAPROCESSNAME + " is not started")
	}
}

func TestIsDeployed(t *testing.T) {
	response := IsDeployed(properties.CABINARYNAME)
	if response {
		print(properties.CABINARYNAME + " is deployed")
	}else{
		print(properties.CABINARYNAME + " is not deployed")
	}
}

func TestExec(t *testing.T) {
	cmd :="cd "+properties.REPOSITORY+" && ls -lisa"
	response, error := syscommand.ExecComplexCmd(cmd)
	print ("response: "+response)
	print ("error: "+error)
}