import json, decimal
import random, arrow, datetime
from config import appconf
from app.common.log import get_logger
logger = get_logger()

class CreateMessageException(Exception):
    pass

class MessageType:
    sysinfo  = 0
    stop     = 1
    exec     = 2
    upload   = 3
    ack      = 4
    error    = 5
    content  = 6

STATUSTOPIC   = "status/"         # status / clientID
ORDERTOPIC    = "orders/"         # orders / clientID
RESPONSETOPIC = "responses/"      # responses / messageID

class Message ():
    def __init__(self, id, agentId, date, mType, body="", error=""):
        self.MessageId = id
        self.AgentId = agentId
        self.Created = date
        self.Mtype   = mType
        self.Body    = body
        self.Error   = error

    def to_str(self):
        return "MessageId={0}, AgentId={1}, Created={2}".format(self.MessageId, self.AgentId, self.Created)

    def to_json(self):
        dict = {}
        dict['MessageId']=self.MessageId
        dict['AgentId']=self.AgentId
        dict['Created']=str(self.Created)
        dict['Mtype']=self.Mtype
        dict['Body']=self.Body
        dict['Error']=self.Error
        return str(dict).replace("'", "\"")


class SysInfo(Message):
    def __init__(self, id, agentId, date):
        mType = MessageType.sysinfo
        super().__init__(id, agentId, date, mType)

    def set_memory_info(self, total, free, used):
        self.total_memory = total
        self.free_memory = free
        self.used_memory = used

    def set_cpus_used(self, **kwargs):
        self.cpu_used=[]
        for key in kwargs:
            self.cpu_used.append(key)

    def set_disk_info(self, total, free, used):
        self.total_disk = total
        self.free_disk = free
        self.used_disk = used

    def set_ca_info(self, is_deploy, is_started):
        self.is_ca_deployed = is_deploy
        self.is_ca_started = is_started

    def set_peer_info(self, is_deploy, is_started):
        self.is_peer_deployed = is_deploy
        self.is_peer_started = is_started

    def set_orderer_info(self, is_deploy, is_started):
        self.is_orderer_deployed = is_deploy
        self.is_orderer_started = is_started

    def to_str(self):
        return "MessageId={0}, AgentId={1}, Date={2}".format(self.MessageId, self.AgentId, self.Date)

class Ack(Message):
    def __init__(self, id, agentId, date):
        mType = MessageType.ack
        super().__init__(id, agentId, date, mType)

    def set_libelle(self, libelle):
        self.libelle = libelle


class Error(Message):
    def __init__(self, id, agentId, date):
        mType = MessageType.error
        super().__init__(id, agentId, date, mType)

    def set_error_libelle(self, libelle):
        self.libelle = libelle


class Content(Message):
    def __init__(self, id, agentId, date, body, error):
        mType = MessageType.content
        super().__init__(id, agentId, date, mType, body, error)

def generateID() :
	return ''.join(random.choice('0123456789ABCDEF') for i in range(16))

def create_message(mtype, body):
    date = arrow.utcnow() # same GO date ormat
    message = Message(id=generateID(), agentId=appconf().AGENTID, date=date, mType=mtype, body=body)
    return message


def build_message(topic, dto_message):
    try:
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
    if MessageType.ack == mtype:
        logger.debug("Received ack on topic: {0}".format(topic))
        return build_ack(id=messageId, agentId=agentId, date=created, mType=mtype, body=body)

    elif MessageType.sysinfo == mtype:
        logger.debug("Received system information on topic: {0}".format(topic))
        return build_sysinfo(id=messageId, agentId=agentId, date=created, mType=mtype, body=body)

    elif MessageType.error == mtype:
        logger.debug("Received error message type on topic: {0}".format(topic))
        return build_error(topic, id=messageId, agentId=agentId, date=created, mType=mtype, error=error)

    elif MessageType.content == mtype:
        logger.debug("Received content message type on topic: {0}".format(topic))
        return build_content(id=messageId, agentId=agentId, date=created, mType=mtype, body=body)

    raise CreateMessageException("bad message type")

def build_ack(id, agentId, date, mType, body):
    logger.debug("Received Ack from agent:"+agentId+" for message:"+id+ " ack="+body)
    ack = Ack(id=id, agentId=agentId, date=date, mType=mType)
    ack.set_libelle(body)
    return ack

def build_sysinfo(id, agentId, date, mType, body):
    sysinfo_dto = json.loads(body)
    logger.debug("Received system info from agent:"+agentId+ "at:"+date+ " info="+str(sysinfo_dto))
    sysinfo = SysInfo(id=id, agentId=agentId, date=date, mType=mType)
    tmem = float(round(decimal.Decimal(sysinfo_dto['TotalMemory']), 3))
    fmem = float(round(decimal.Decimal(sysinfo_dto['FreeMemory']), 3))
    umem = float(round(decimal.Decimal(sysinfo_dto['UsedMemory']), 3))
    tdisk = float(round(decimal.Decimal(sysinfo_dto['TotalDisk']), 3))
    fdisk = float(round(decimal.Decimal(sysinfo_dto['FreeDisk']), 3))
    udisk = float(round(decimal.Decimal(sysinfo_dto['UsedDisk']), 3))
    cpuused = sysinfo_dto['CpusUtilisation']

    sysinfo.set_ca_info(is_deploy=sysinfo_dto['Ca_deployed'], is_started=sysinfo_dto['Ca_started'])
    sysinfo.set_peer_info(is_deploy=sysinfo_dto['Peer_deployed'], is_started=sysinfo_dto['Peer_started'])
    sysinfo.set_orderer_info(is_deploy=sysinfo_dto['Orderer_deployed'], is_started=sysinfo_dto['Orderer_started'])
    sysinfo.set_memory_info(tmem, fmem, umem)
    sysinfo.set_disk_info(tdisk, fdisk, udisk)
    sysinfo.set_cpus_used(cpuused)
    return sysinfo


def build_content(id, agentId, date, mType, body):
    logger.debug("Received content from agent:" + agentId + "at:" + date )
    content = Content(id=id, agentId=agentId, date=date, mType=mType)
    content_dto = json.loads(body)
    return content



def build_error(topic, id, agentId, date, mType, error):
    error = Error(id=id, agentId=agentId, date=date, mType=mType)
    error.set_error_libelle(error)
    if STATUSTOPIC in topic:
        logger.debug("Received error during system info generation on agent:"+agentId+ " err="+error)
    else:
        logger.debug("Received error for message:"+id+ " on agent:"+agentId+" err="+error)
    return error
