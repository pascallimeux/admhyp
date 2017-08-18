package syscommand

import (
        "github.com/shirou/gopsutil/cpu"
        "github.com/shirou/gopsutil/disk"
        "github.com/shirou/gopsutil/mem"
	"encoding/json"
	"github.com/pascallimeux/admhyp/agent/logger"
)
type SysInfo struct{
	TotalMemory		float64
	FreeMemory      	float64
	UsedMemory      	float64
	TotalDisk       	float64
	FreeDisk        	float64
	UsedDisk		float64
	CpusUtilisation 	[]float64
	Ca_deployed     	bool
	Ca_started		bool
	Orderer_deployed	bool
	Orderer_started		bool
	Peer_deployed		bool
	Peer_started		bool
}

func (s SysInfo)ToJsonStr() string{
	json_mess, err := json.Marshal(s)
    	if err != nil {
		logger.Log.Error(err)
		return ""
    	}
	return string(json_mess)
}

func GetSystemStatus() (SysInfo, error) {
	sysInfo := SysInfo{}
	vmStat, err := mem.VirtualMemory()
        if (err != nil){
		logger.Log.Error(err)
		return sysInfo, err
	}
	sysInfo.TotalMemory = float64(vmStat.Total)/1024/1024/1024
	sysInfo.FreeMemory = float64(vmStat.Free)/1024/1024/1024
	sysInfo.UsedMemory = vmStat.UsedPercent
	diskStat, err := disk.Usage("/")
	if (err != nil){
		logger.Log.Error(err)
		return sysInfo, err
	}
	sysInfo.TotalDisk = float64(diskStat.Total)/1024/1024/1024
	sysInfo.FreeDisk = float64(diskStat.Free)/1024/1024/1024
	sysInfo.UsedDisk = diskStat.UsedPercent
        percentage, err := cpu.Percent(0, true)
	if (err != nil){
		logger.Log.Error(err)
		return sysInfo, err
	}
	sysInfo.CpusUtilisation = make ([]float64, len(percentage))
	for idx, cpupercent := range percentage {
		sysInfo.CpusUtilisation[idx]= cpupercent
        }
	sysInfo.Ca_deployed = false
	sysInfo.Ca_started = false
	sysInfo.Orderer_deployed = false
	sysInfo.Orderer_started = false
	sysInfo.Peer_deployed = false
	sysInfo.Peer_started = false
	return sysInfo, nil


}
