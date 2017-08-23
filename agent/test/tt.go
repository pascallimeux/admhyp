package main

import (
	"strings"
	"os/exec"
	"sync"
	"fmt"
)

func ExecCmd(cmd string) {
	parts := strings.Fields(cmd)
	head := parts[0]
	parts = parts[1:len(parts)]
	out, err := exec.Command(head, parts...).CombinedOutput()
	print ("err= " +err.Error()+"\n")
	print ("out= " +string(out))
}

func exe_cmd(cmd string, wg *sync.WaitGroup) {
  fmt.Println("command is ",cmd)
  // splitting head => g++ parts => rest of the command
  parts := strings.Fields(cmd)
  head := parts[0]
  parts = parts[1:len(parts)]

  out, err := exec.Command(head,parts...).Output()
  if err != nil {
    fmt.Printf("%s", err)
  }
  fmt.Printf("%s", out)
  wg.Done() // Need to signal to waitgroup that this goroutine is done
}

func main() {

	//cmd := "sh -c kill -9 `pidof hyp-agent` 2>/dev/null"
	//cmd2 :="PID=`pidof hyp-agent` && [ -n \"$PID\" ] && echo True || echo False"
	cmd3 :="cd /var/hyperledger && CMD=\"./bin/fabric-ca-server start -b toto:'password' -c .keys/config.yaml > log/ca.log 2>&1 &\" && eval \"$CMD\""
	out, err := exec.Command("sh","-c",cmd3).Output()
	if err != nil {
    		fmt.Printf("%s", err)
  	}
  	fmt.Printf("%s", out)
}
