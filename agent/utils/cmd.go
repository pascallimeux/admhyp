package utils

import (
	"os/exec"
	"os/user"
	"sync"
	"strings"
	"fmt"
	"os"
	"errors"
	"io/ioutil"
	"syscall"
	"strconv"
	"path/filepath"
)

func ExecDetachCmd(username, cmd string) error {
	log.Debug("user "+username+" execute "+cmd)
	user, err := user.Lookup(username)
	uid, err  := strconv.ParseUint(user.Uid, 10, 32)
    	if err != nil {
		log.Error(err)
		return err
   	}
	gid, err  := strconv.ParseUint(user.Gid, 10, 32)
    	if err != nil {
		log.Error(err)
		return err
   	}
	if err != nil {
		log.Error(err)
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
		log.Error(err)
		return err
	}
	return nil
}

func ExecCmd2(cmd string, wg *sync.WaitGroup) ([]byte, error){
	log.Debug("exec local command: "+cmd)
	parts := strings.Fields(cmd)
	head := parts[0]
	parts = parts[1:len(parts)]
	out, err := exec.Command(head, parts...).CombinedOutput()
	if err != nil {
		log.Error(err)
	}
	wg.Done()
	return out, err
}

func ExecCmd(cmd string) ([]byte, error){
	log.Debug("exec local command: "+cmd)
	parts := strings.Fields(cmd)
	head := parts[0]
	parts = parts[1:len(parts)]
	out, err := exec.Command(head, parts...).CombinedOutput()
	if err != nil {
		log.Error(err.Error())
		log.Error(string(out))
		return nil, errors.New(string(out))
	}
	return out, err
}

func IsServiceActif(servicename string) (bool, error){
	cmd :="sudo systemctl is-active "+servicename
	out, err := ExecCmd(cmd)
	if err != nil {
		log.Error(err)
		return false, err
	}
	return !strings.Contains(fmt.Sprint(out), "inactive"), nil
}

func GetSystemUsername()(string, error){
	usr, err := user.Current()
	if err != nil {
		log.Error(err)
		return "", err
	}
	return usr.Name, nil
}


func CreateDirectory(path string)(bool, error){
	if _, err := os.Stat(path); os.IsNotExist(err) {
		cmd := "sudo mkdir -p " + path
		_, err := ExecCmd(cmd)
		if err != nil {
			log.Error(err)
			return false, err
		}
		cmd1 := "sudo chmod 777 " + path
		_, err = ExecCmd(cmd1)
		if err != nil {
			log.Error(err)
			return false, err
		}
		log.Info(fmt.Sprint("create directory "+path))
		return true, nil
	}
	log.Info(fmt.Sprint("Directory "+path+" already exist..."))
	return false, nil
}

func CreateAccount(username string) (bool, error){
	_, err := user.Lookup(username)
	if err == nil {
		log.Info(fmt.Sprint("user "+username+" already exist..."))
		return false, nil
	}else{
		cmd :="sudo useradd -m "+username+" -s /bin/bash"
		_, err = ExecCmd(cmd)
		if err != nil {
			log.Error(err)
			return false, err
		}
		log.Info(fmt.Sprint("create user "+username))
	}
	return true, nil
}

func CreateFile(filename, content string) (bool, error){
	if _, err := os.Stat(filename); err == nil {
		log.Info(fmt.Sprint("file " + filename + " already exists!"))
		return false, nil
	}
	err := ioutil.WriteFile(filename, []byte(content), 0644)
	if err != nil {
		log.Error(err)
		return false, err
	}
	log.Info(fmt.Sprint("create file " + filename))
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
			log.Error(err)
			return err
		}
		_, err = ExecCmd(cmd1)
		if err != nil {
			log.Error(err)
			return err
		}
		_, err = ExecCmd(cmd2)
		if err != nil {
			log.Error(err)
			return err
		}
		_, err = ExecCmd(cmd3)
		if err != nil {
			log.Error(err)
			return err
		}
		log.Info(fmt.Sprint("create file " + filename))
	}else{
		log.Info(fmt.Sprint("file " + filename + " already exists!"))
	}
	return nil
}

func addKey(ssh_file, pubkey string) (bool, error){
	create, err := CreateFile(ssh_file, pubkey)
	if err != nil {
		log.Error(err)
		return false, err
	}
	if create {
		return true, nil
	}
	cmd := "sudo chmod 777 "+ ssh_file
	_, err = ExecCmd(cmd)
	if err != nil {
		log.Error(err)
		return false, err
	}
	b, err := ioutil.ReadFile(ssh_file)
	if err != nil {
		log.Error(err)
        	return false, err
    	}
    	s := string(b)
	if (strings.Contains(s, pubkey)){
		log.Info(fmt.Sprint("key already authorized!"))
		return false, nil
	}
	err = AppendStringToFile(ssh_file, pubkey)
	if err != nil {
		log.Error(err)
        	return false, err
    	}
	log.Info(fmt.Sprint("key added in "+ssh_file))
	return true, nil
}

func AppendStringToFile(path, text string) error {
      f, err := os.OpenFile(path, os.O_APPEND|os.O_WRONLY, os.ModeAppend)
      if err != nil {
	      log.Error(err)
              return err
      }
      defer f.Close()

      _, err = f.WriteString(text)
      if err != nil {
	      log.Error(err)
	      return err
      }
      return nil
}

func AuthorizedKey(username, pubkey string) error {
	ssh_dir:= "/home/"+username+"/.ssh"
	ssh_file := ssh_dir+"/"+"authorized_keys"
	_, err := CreateDirectory(ssh_dir)
	if err != nil {
		log.Error(err)
		return err
	}
	cmd0 := "sudo chmod 777 "+ ssh_dir
	_, err = ExecCmd(cmd0)
	if err != nil {
		log.Error(err)
		return err
	}
	_, err = addKey(ssh_file, pubkey)
	if err != nil {
		log.Error(err)
		return err
	}
	cmd1 := "sudo chown -R "+username+"."+username+" "+ ssh_dir
	cmd2 := "sudo chmod 700 " + ssh_dir
	cmd3 := "sudo chmod 600 "+ ssh_file
	_, err = ExecCmd(cmd1)
	if err != nil {
		log.Error(err)
		return err
	}
	_, err = ExecCmd(cmd2)
	if err != nil {
		log.Error(err)
		return err
	}
	_, err = ExecCmd(cmd3)
	if err != nil {
		log.Error(err)
		return err
	}
	return nil
}

func GetProgrammFullName() (string, error) {
	ex, err := os.Executable()
	if err != nil {
		return "", nil
	}
        exPath := filepath.Dir(ex)
	return exPath, nil
}


func MoveFile(source, destination string) error {
	err := os.Rename(source, destination)
	if err != nil {
		return err
	}
	return nil
}