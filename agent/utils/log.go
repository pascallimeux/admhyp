package utils
import (
	"github.com/op/go-logging"
	"os"
	"strings"
)

var format = logging.MustStringFormatter(
	`%{color}%{time:15:04:05.000} %{shortfunc} %{shortfile} ▶ %{level:.4s} %{id:03x}%{color:reset} %{message}`,
)

var log *logging.Logger

func InitLog(module, level string) *logging.Logger{
	logLevel := logging.ERROR
	switch strings.ToUpper(level) {
	case "DEBUG":
		logLevel = logging.DEBUG
	case "INFO":
		logLevel = logging.INFO
	case "CRITICAL":
		logLevel = logging.CRITICAL
	case "WARNING":
		logLevel = logging.WARNING
	}
	log = logging.MustGetLogger(module)
	backend := logging.NewLogBackend(os.Stderr, "", 0)
	backendFormatter := logging.NewBackendFormatter(backend, format)
	backendLeveled := logging.AddModuleLevel(backendFormatter)
	backendLeveled.SetLevel(logLevel, "")
	logging.SetBackend(backendLeveled)
	return log
}

func GetLogger() *logging.Logger{
	return log
}