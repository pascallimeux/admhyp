package system

import (
        "github.com/shirou/gopsutil/cpu"
        "github.com/shirou/gopsutil/disk"
        "github.com/shirou/gopsutil/mem"
	"github.com/pascallimeux/admhyp/agent/mqtt"
	"github.com/pascallimeux/admhyp/agent/log"
	"strconv"
	"encoding/json"
)
type SysInfo struct{
	TotalMemory	string
	FreeMemory      string
	UsedMemory      string
	TotalDisk       string
	FreeDisk        string
	UsedDisk	string
	CpusUtilisation []string
}

func (s SysInfo)ToJsonStr() string{
	json_mess, err := json.Marshal(s)
    	if err != nil {
		log.Error(err)
		return ""
    	}
	return string(json_mess)
}

func GetSystemStatus() *mqtt.Message {
	sysInfo := SysInfo{}
	message := &mqtt.Message{Id:mqtt.GenerateID(16)}
	vmStat, err := mem.VirtualMemory()
        if (err != nil){
		message.Error = err.Error()
		log.Error(err)
		return message
	}
	sysInfo.TotalMemory = strconv.FormatUint(vmStat.Total/1000000000, 10) + " Gb"
	sysInfo.FreeMemory = strconv.FormatUint(vmStat.Free/1000000000, 10) + " Gb"
	sysInfo.UsedMemory = strconv.FormatFloat(vmStat.UsedPercent, 'f', 2, 64) + "%"
	diskStat, err := disk.Usage("/")
	if (err != nil){
		message.Error = err.Error()
		log.Error(err)
		return message
	}
	sysInfo.TotalDisk = strconv.FormatUint(diskStat.Total/1000000000, 10) + " Gb"
	sysInfo.FreeDisk = strconv.FormatUint(diskStat.Free/1000000000, 10) + " Gb"
	sysInfo.UsedDisk = strconv.FormatFloat(diskStat.UsedPercent, 'f', 2, 64) + "%"
        percentage, err := cpu.Percent(0, true)
	if (err != nil){
		message.Error = err.Error()
		log.Error(err)
		return message
	}
	sysInfo.CpusUtilisation = make ([]string, len(percentage))
	for idx, cpupercent := range percentage {
		sysInfo.CpusUtilisation[idx]= strconv.FormatFloat(cpupercent, 'f', 2, 64) + "%"
        }
	message.Body=sysInfo.ToJsonStr()
	json_mess, _ := json.Marshal(sysInfo)
	log.Debug(string(json_mess))
	return message

}
