package syscommand

import (
	"os/exec"
	"syscall"
	"github.com/pascallimeux/admhyp/agent/logger"
	"strings"
	"strconv"
	"os/user"
	"errors"
)

func ExecDetachCmd(username, cmd string) error {
	logger.Log.Debug("user "+username+" execute "+cmd)
	user, err := user.Lookup(username)
	uid, err  := strconv.ParseUint(user.Uid, 10, 32)
    	if err != nil {
		logger.Log.Error(err)
		return err
   	}
	gid, err  := strconv.ParseUint(user.Gid, 10, 32)
    	if err != nil {
		logger.Log.Error(err)
		return err
   	}
	if err != nil {
		logger.Log.Error(err)
		return err
	}
	result := exec.Command("sh", "-c", cmd)
	result.SysProcAttr = &syscall.SysProcAttr{}
    	result.SysProcAttr.Credential = &syscall.Credential{Uid: uint32(uid), Gid: uint32(gid)}
	//result.Stdin = os.Stdin
	//result.Stdout = os.Stdout
	//result.Stderr = os.Stderr
	err = result.Start()
	if err != nil {
		logger.Log.Error(err)
		return err
	}
	return nil
}

func ExecComplexCmd(cmd string)  (string, string){
	logger.Log.Debug("exec local command: "+cmd)
	out, err := exec.Command("sh","-c",cmd).CombinedOutput()
	if err != nil {
		logger.Log.Error(err)
		logger.Log.Error(errors.New(string(out)))
		return "",string(out)
	}
	logger.Log.Debug("out= "+string(out))
	return string(out), ""
}

func ExecCmd(cmd string) ([]byte, error){
	logger.Log.Debug("exec local command: "+cmd)
	parts := strings.Fields(cmd)
	head := parts[0]
	parts = parts[1:len(parts)]
	out, err := exec.Command(head, parts...).CombinedOutput()
	if err != nil {
		logger.Log.Error(err)
		logger.Log.Error(errors.New(string(out)))
		return nil, errors.New(string(out))
	}
	return out, err
}

func Compress(src, dst string) error {
	cmd := "tar czf "+src+" "+dst
	_, err :=ExecCmd(cmd)
	return err
}

func Uncompress(tgz, dst string) error{
	cmd := "tar xzf "+tgz+" "+dst
	_, err :=ExecCmd(cmd)
	return err
}