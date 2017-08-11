package utils

import (
	"os/exec"
	"os/user"
	"sync"
	"strings"
	"github.com/op/go-logging"
	"fmt"
	"os"
)
var log = logging.MustGetLogger("agent")

func Exec_detach_cmd(cmd string) error {
	log.Debug("exec detach command: "+cmd)
	result := exec.Command("sh", "-c", cmd)
	//result.Stdin = os.Stdin
	//result.Stdout = os.Stdout
	//result.Stderr = os.Stderr
	err := result.Start()
	if err != nil {
		return err
	}
	return nil
}

func Exec_cmd(cmd string, wg *sync.WaitGroup) ([]byte, error){
	log.Debug("exec local command: "+cmd)
	parts := strings.Fields(cmd)
	head := parts[0]
	parts = parts[1:len(parts)]
	out, err := exec.Command(head,parts...).Output()
	if err != nil {
		log.Error(err)
	}
	wg.Done()
	return out, err
}


func Is_service_active(servicename string) (bool, error){
	wg := new(sync.WaitGroup)
	cmd :="sudo systemctl is-active "+servicename
	out, err := Exec_cmd(cmd, wg)
	if err != nil {
		return false, err
	}
	return !strings.Contains(fmt.Sprint(out), "inactive"), nil
}

func Get_system_username()(string, error){
	usr, err := user.Current()
	if err != nil {
		return "", err
	}
	return usr.Name, nil
}


func Create_directory(path string)(bool, error){
	if _, err := os.Stat(path); os.IsNotExist(err) {
		wg := new(sync.WaitGroup)
		wg.Add(1)
		cmd := "sudo mkdir -p " + path
		_, err := Exec_cmd(cmd, wg)
		if err != nil {
			return false, err
		}
		wg.Wait()
		log.Debug(fmt.Sprint("create directory "+path))
		return true, nil
	}
	log.Debug(fmt.Sprint("Directory "+path+" already exist..."))
	return false, nil
}

func Create_admin_account(username, pubkey string) error{
	_, err := user.Lookup(username)
	if err == nil {
		log.Debug(fmt.Sprint("user: "+username+" already exist..."))
		return nil
	}
	wg := new(sync.WaitGroup)
	wg.Add(1)
	cmd :="sudo useradd -m "+username+" -s /bin/bash"
	_, err = Exec_cmd(cmd, wg)
	if err != nil {
		return err
	}
	wg.Wait()
	log.Debug(fmt.Sprint("create user "+username))
	return nil
}