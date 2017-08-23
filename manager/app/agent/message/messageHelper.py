import json, decimal
import random, arrow
from config import appconf
from app.agent.message.messages import Order_dto, Response_dto, SysInfo_dto
from app.common.log import get_logger
logger = get_logger()

class CreateResponseException(Exception):
    pass

def generateID() :
	return ''.join(random.choice('0123456789ABCDEF') for i in range(16))

def create_order_dto(order, args):
    date = arrow.utcnow() # same GO date ormat
    messageId = generateID()
    agentId = appconf().AGENTID
    order_dto = Order_dto(id=messageId, agentId=agentId, date=date, order=order, args=args)
    return order_dto


def build_sysinfo_dto(sysinfo_raw):
    try:
        sysinfo_dict = json.loads(sysinfo_raw.decode(encoding='UTF-8'))
        agentId = sysinfo_dict['AgentId']
        date = arrow.get(sysinfo_dict['Created'])
        sysinfo_dto = SysInfo_dto(id=id, agentId=agentId, date=date)
        tmem = float(round(decimal.Decimal(sysinfo_dict['TotalMemory']), 2))
        fmem = float(round(decimal.Decimal(sysinfo_dict['FreeMemory']), 2))
        umem = float(round(decimal.Decimal(sysinfo_dict['UsedMemory']), 2))
        tdisk = float(round(decimal.Decimal(sysinfo_dict['TotalDisk']), 2))
        fdisk = float(round(decimal.Decimal(sysinfo_dict['FreeDisk']), 2))
        udisk = float(round(decimal.Decimal(sysinfo_dict['UsedDisk']), 2))
        cpuused = []
        for cpu_use in sysinfo_dict['CpusUtilisation']:
            cpuused.append(str(float(round(decimal.Decimal(cpu_use), 2)))+" ")
        sysinfo_dto.set_ca_info(is_deploy=sysinfo_dict['Ca_deployed'], is_started=sysinfo_dict['Ca_started'])
        sysinfo_dto.set_peer_info(is_deploy=sysinfo_dict['Peer_deployed'], is_started=sysinfo_dict['Peer_started'])
        sysinfo_dto.set_orderer_info(is_deploy=sysinfo_dict['Orderer_deployed'], is_started=sysinfo_dict['Orderer_started'])
        sysinfo_dto.set_memory_info(tmem, fmem, umem)
        sysinfo_dto.set_disk_info(tdisk, fdisk, udisk)
        sysinfo_dto.set_cpus_used(cpuused)
        return sysinfo_dto
    except Exception as e:
        raise CreateResponseException(e)


def build_response_dto(response_raw):
    try:
        response_dict = json.loads(response_raw.decode(encoding='UTF-8'))
        messageId = response_dict['MessageId']
        agentId = response_dict['AgentId']
        created = arrow.get(response_dict['Created'])
        order = response_dict['Order']
        response = response_dict['Response']
        error = response_dict['Error']
        content = response_dict['Content']
        response_dto = Response_dto(id=messageId, agentId=agentId, date=created, order=order, error=error, response=response, content=content)
        return response_dto
    except Exception as e:
        raise CreateResponseException(e)
