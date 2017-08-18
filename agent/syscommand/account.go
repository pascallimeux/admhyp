package syscommand

import (
	"github.com/pascallimeux/admhyp/agent/logger"
	"fmt"
	"os"
	"io/ioutil"
	"strings"
	"os/user"
)

func CreateAccount(username string) (bool, error){
	_, err := user.Lookup(username)
	if err == nil {
		logger.Log.Info(fmt.Sprint("user "+username+" already exist..."))
		return false, nil
	}else{
		cmd :="sudo useradd -m "+username+" -s /bin/bash"
		_, err = ExecCmd(cmd)
		if err != nil {
			logger.Log.Error(err)
			return false, err
		}
		logger.Log.Info(fmt.Sprint("create user "+username))
	}
	return true, nil
}


func AddSudo(username string) error{
	filename := "/etc/sudoers.d/"+username
	tmpfile  := "/tmp/"+username
	if _, err := os.Stat(filename); os.IsNotExist(err) {
		line := username+" ALL=(ALL:ALL) NOPASSWD:ALL"
		cmd1 := "sudo chown root.root "+ tmpfile
		cmd2 := "sudo chmod ug-w "+ tmpfile
		cmd3 := "sudo mv "+ tmpfile + " /etc/sudoers.d/" + username
		_, err = CreateFile(tmpfile, line)
		if err != nil {
			logger.Log.Error(err)
			return err
		}
		_, err = ExecCmd(cmd1)
		if err != nil {
			logger.Log.Error(err)
			return err
		}
		_, err = ExecCmd(cmd2)
		if err != nil {
			logger.Log.Error(err)
			return err
		}
		_, err = ExecCmd(cmd3)
		if err != nil {
			logger.Log.Error(err)
			return err
		}
		logger.Log.Info(fmt.Sprint("create file " + filename))
	}else{
		logger.Log.Info(fmt.Sprint("file " + filename + " already exists!"))
	}
	return nil
}

func addKey(ssh_file, pubkey string) (bool, error){
	create, err := CreateFile(ssh_file, pubkey)
	if err != nil {
		logger.Log.Error(err)
		return false, err
	}
	if create {
		return true, nil
	}
	cmd := "sudo chmod 777 "+ ssh_file
	_, err = ExecCmd(cmd)
	if err != nil {
		logger.Log.Error(err)
		return false, err
	}
	b, err := ioutil.ReadFile(ssh_file)
	if err != nil {
		logger.Log.Error(err)
        	return false, err
    	}
    	s := string(b)
	if (strings.Contains(s, pubkey)){
		logger.Log.Info(fmt.Sprint("key already authorized!"))
		return false, nil
	}
	err = appendStringToFile(ssh_file, pubkey)
	if err != nil {
		logger.Log.Error(err)
        	return false, err
    	}
	logger.Log.Info(fmt.Sprint("key added in "+ssh_file))
	return true, nil
}

func AuthorizedKey(username, pubkey string) error {
	ssh_dir:= "/home/"+username+"/.ssh"
	ssh_file := ssh_dir+"/"+"authorized_keys"
	_, err := CreateDirectory(ssh_dir)
	if err != nil {
		logger.Log.Error(err)
		return err
	}
	cmd0 := "sudo chmod 777 "+ ssh_dir
	_, err = ExecCmd(cmd0)
	if err != nil {
		logger.Log.Error(err)
		return err
	}
	_, err = addKey(ssh_file, pubkey)
	if err != nil {
		logger.Log.Error(err)
		return err
	}
	cmd1 := "sudo chown -R "+username+"."+username+" "+ ssh_dir
	cmd2 := "sudo chmod 700 " + ssh_dir
	cmd3 := "sudo chmod 600 "+ ssh_file
	_, err = ExecCmd(cmd1)
	if err != nil {
		logger.Log.Error(err)
		return err
	}
	_, err = ExecCmd(cmd2)
	if err != nil {
		logger.Log.Error(err)
		return err
	}
	_, err = ExecCmd(cmd3)
	if err != nil {
		logger.Log.Error(err)
		return err
	}
	return nil
}

