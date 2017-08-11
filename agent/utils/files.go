package utils

import (
	"path/filepath"
	"os"
	"strings"
)

// Get the directory of the programm
func GetProgrammDirectory() (string, error) {
	pwd, err := filepath.Abs(filepath.Dir(os.Args[0]))
	return pwd, err
}

// Get the name of the Programm
func GetProgrammName() (string, error) {
	progCmd := strings.Split(os.Args[0], "\\")
	progName := progCmd[len(progCmd)-1]
	return progName, nil
}

// Get the full name of the Programm
func GetProgrammFullName() (string, error) {
	progName := ""
	pwd, err := GetProgrammDirectory()
	if err != nil {
		return pwd, err
	}
	progName, err = GetProgrammName()
	if err != nil {
		return pwd, err
	}
	pwd += "\\" + progName
	pwd = strings.TrimSpace(pwd)
	return pwd, nil
}


func MoveFile(source, destination string) error {
	err := os.Rename(source, destination)
	if err != nil {
		return err
	}
	return nil
}