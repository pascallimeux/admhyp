package logger
import (
	"github.com/op/go-logging"
	"os"
	"strings"
)

var format = logging.MustStringFormatter(
	`%{color}%{time:15:04:05.000} %{shortfunc} %{shortfile} ▶ %{level:.4s} %{id:03x}%{color:reset} %{message}`,
)

var Log *logging.Logger

func InitLog(module, level string) {
	logLevel := logging.ERROR
	switch strings.ToUpper(level) {
	case "DEBUG":
		logLevel = logging.DEBUG
	case "INFO":
		logLevel = logging.INFO
	case "WARNING":
		logLevel = logging.WARNING
	}
	Log = logging.MustGetLogger(module)
	backend := logging.NewLogBackend(os.Stderr, "", 0)
	backendFormatter := logging.NewBackendFormatter(backend, format)
	backendLeveled := logging.AddModuleLevel(backendFormatter)
	backendLeveled.SetLevel(logLevel, "")
	logging.SetBackend(backendLeveled)
}
