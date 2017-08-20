import json, decimal
import random, arrow, datetime
from config import appconf
from app.agent.message.messages import Message, MessageType, Ack, Content, Error, SysInfo, STATUSTOPIC
from app.common.log import get_logger
logger = get_logger()

class CreateMessageException(Exception):
    pass

def generateID() :
	return ''.join(random.choice('0123456789ABCDEF') for i in range(16))

def create_sended_message(mtype, body):
    date = arrow.utcnow() # same GO date ormat
    message = Message(id=generateID(), agentId=appconf().AGENTID, date=date, mType=mtype, body=body)
    return message


def build_received_message(topic, dto_message):
    try:
        logger.debug("Received message_dto:{}".format(str(dto_message)))
        message_dto = json.loads(dto_message.decode(encoding='UTF-8'))
        messageId = message_dto['MessageId']
        agentId = message_dto['AgentId']
        created = arrow.get(message_dto['Created'])
        mtype = message_dto['Mtype']
        if "Error" in message_dto:
            error = message_dto['Error']
        if "Body" in message_dto:
            body = message_dto['Body']
    except Exception as e:
        raise CreateMessageException(e)
    if MessageType.ACK.value == mtype:
        logger.debug("Received ack on topic: {0}".format(topic))
        return build_ack(id=messageId, agentId=agentId, date=created, body=body)

    elif MessageType.SYSINFO.value == mtype:
        logger.debug("Received system information on topic: {0}".format(topic))
        return build_sysinfo(id=messageId, agentId=agentId, date=created, body=body)

    elif MessageType.ERROR.value == mtype:
        logger.debug("Received error message type on topic: {0}".format(topic))
        return build_error(topic, id=messageId, agentId=agentId, date=created, error=error)

    elif MessageType.CONTENT.value == mtype:
        logger.debug("Received content message type on topic: {0}".format(topic))
        return build_content(id=messageId, agentId=agentId, date=created, body=body)

    raise CreateMessageException("bad message type")

def build_ack(id, agentId, date, body):
    logger.debug("Received Ack from agent:"+agentId+" for message:"+id+ " ack="+body)
    ack = Ack(id=id, agentId=agentId, date=date)
    ack.set_libelle(body)
    return ack

def build_sysinfo(id, agentId, date, body):
    sysinfo_dto = json.loads(body)
    logger.debug("Received system info from agent:"+agentId+ "at:"+str(date)+ " info="+str(sysinfo_dto))
    sysinfo = SysInfo(id=id, agentId=agentId, date=date)
    tmem = float(round(decimal.Decimal(sysinfo_dto['TotalMemory']), 2))
    fmem = float(round(decimal.Decimal(sysinfo_dto['FreeMemory']), 2))
    umem = float(round(decimal.Decimal(sysinfo_dto['UsedMemory']), 2))
    tdisk = float(round(decimal.Decimal(sysinfo_dto['TotalDisk']), 2))
    fdisk = float(round(decimal.Decimal(sysinfo_dto['FreeDisk']), 2))
    udisk = float(round(decimal.Decimal(sysinfo_dto['UsedDisk']), 2))
    cpuused = []
    for cpu_use in sysinfo_dto['CpusUtilisation']:
        cpuused.append(str(float(round(decimal.Decimal(cpu_use), 2)))+" ")

    sysinfo.set_ca_info(is_deploy=sysinfo_dto['Ca_deployed'], is_started=sysinfo_dto['Ca_started'])
    sysinfo.set_peer_info(is_deploy=sysinfo_dto['Peer_deployed'], is_started=sysinfo_dto['Peer_started'])
    sysinfo.set_orderer_info(is_deploy=sysinfo_dto['Orderer_deployed'], is_started=sysinfo_dto['Orderer_started'])
    sysinfo.set_memory_info(tmem, fmem, umem)
    sysinfo.set_disk_info(tdisk, fdisk, udisk)
    sysinfo.set_cpus_used(cpuused)
    return sysinfo


def build_content(id, agentId, date, body):
    logger.debug("Received content from agent:" + agentId + "at:" + date )
    content = Content(id=id, agentId=agentId, date=date, body=body)
    content_dto = json.loads(body)
    return content


def build_error(topic, id, agentId, date, mError):
    error = Error(id=id, agentId=agentId, date=date)
    error.set_error_libelle(mError)
    if STATUSTOPIC in topic:
        logger.debug("Received error during system info generation on agent:"+agentId+ " err="+mError)
    else:
        logger.debug("Received error for message:"+id+ " on agent:"+agentId+" err="+mError)
    return error