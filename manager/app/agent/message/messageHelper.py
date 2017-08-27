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
    date = arrow.now() # same GO date ormat
    messageId = generateID()
    agentId = appconf().AGENTID
    order_dto = Order_dto(id=messageId, agentId=agentId, date=date, order=order, args=args)
    return order_dto


def build_sysinfo_dto(sysinfo_raw):
    try:
        sysinfo_dict = json.loads(sysinfo_raw.decode(encoding='UTF-8'))
        agentId = sysinfo_dict['agentid']
        date = arrow.get(sysinfo_dict['created'])
        sysinfo_dto = SysInfo_dto(id=id, agentId=agentId, date=date)
        tmem = float(round(decimal.Decimal(sysinfo_dict['totalmemory']), 2))
        fmem = float(round(decimal.Decimal(sysinfo_dict['freememory']), 2))
        umem = float(round(decimal.Decimal(sysinfo_dict['usedmemory']), 2))
        tdisk = float(round(decimal.Decimal(sysinfo_dict['totaldisk']), 2))
        fdisk = float(round(decimal.Decimal(sysinfo_dict['freedisk']), 2))
        udisk = float(round(decimal.Decimal(sysinfo_dict['useddisk']), 2))
        cpuused = []
        for cpu_use in sysinfo_dict['cpusutilisation']:
            cpuused.append(str(float(round(decimal.Decimal(cpu_use), 2)))+" ")
        sysinfo_dto.set_ca_info(is_deploy=sysinfo_dict['cadeployed'], is_started=sysinfo_dict['castarted'])
        sysinfo_dto.set_peer_info(is_deploy=sysinfo_dict['peerdeployed'], is_started=sysinfo_dict['peerstarted'])
        sysinfo_dto.set_orderer_info(is_deploy=sysinfo_dict['ordererdeployed'], is_started=sysinfo_dict['ordererstarted'])
        sysinfo_dto.set_memory_info(tmem, fmem, umem)
        sysinfo_dto.set_disk_info(tdisk, fdisk, udisk)
        sysinfo_dto.set_cpus_used(cpuused)
        return sysinfo_dto
    except Exception as e:
        raise CreateResponseException(e)


def build_response_dto(response_raw):
    try:
        content = error = None
        response_dict = json.loads(response_raw.decode(encoding='UTF-8'))
        messageId = response_dict['messageid']
        agentId = response_dict['agentid']
        created = arrow.get(response_dict['created'])
        order = response_dict['order']
        response = response_dict['response']
        if 'error' in response_dict:
            error = response_dict['error']
        if 'content' in response_dict:
            content = response_dict['content']
        response_dto = Response_dto(id=messageId, agentId=agentId, date=created, order=order, error=error, response=response, content=content)
        return response_dto
    except Exception as e:
        raise CreateResponseException(e)
