package syscommand

import (
	"os"
	"github.com/pascallimeux/admhyp/agent/logger"
	"fmt"
	"io/ioutil"
	"path/filepath"
)

func CreateDirectory(path string)(bool, error){
	if _, err := os.Stat(path); os.IsNotExist(err) {
		cmd := "sudo mkdir -p " + path
		_, err := ExecCmd(cmd)
		if err != nil {
			logger.Log.Error(err)
			return false, err
		}
		cmd1 := "sudo chmod 777 " + path
		_, err = ExecCmd(cmd1)
		if err != nil {
			logger.Log.Error(err)
			return false, err
		}
		logger.Log.Info(fmt.Sprint("create directory "+path))
		return true, nil
	}
	logger.Log.Info(fmt.Sprint("Directory "+path+" already exist..."))
	return false, nil
}


func CreateFile(filename, content string) (bool, error){
	if _, err := os.Stat(filename); err == nil {
		logger.Log.Info(fmt.Sprint("file " + filename + " already exists!"))
		return false, nil
	}
	err := ioutil.WriteFile(filename, []byte(content), 0644)
	if err != nil {
		logger.Log.Error(err)
		return false, err
	}
	logger.Log.Info(fmt.Sprint("create file " + filename))
	return true, nil
}


func appendStringToFile(path, text string) error {
      f, err := os.OpenFile(path, os.O_APPEND|os.O_WRONLY, os.ModeAppend)
      if err != nil {
	      logger.Log.Error(err)
              return err
      }
      defer f.Close()

      _, err = f.WriteString(text)
      if err != nil {
	      logger.Log.Error(err)
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
