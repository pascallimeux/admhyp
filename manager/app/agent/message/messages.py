from enum import Enum
from app.common.log import get_logger
logger = get_logger()

class CreateMessageException(Exception):
    pass

class MessageType(Enum):
    SYSINFO  = 0
    STOP     = 1
    EXEC     = 2
    UPLOAD   = 3
    ACK      = 4
    ERROR    = 5
    CONTENT  = 6

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
        return "MessageId={0}, AgentId={1}, Created={2} Type={3}".format(self.MessageId, self.AgentId, self.Created, self.Mtype.name)

    def to_json(self):
        dict = {}
        dict['MessageId']=self.MessageId
        dict['AgentId']=self.AgentId
        dict['Created']=str(self.Created)
        dict['Mtype']=self.Mtype.value
        dict['Body']=self.Body
        dict['Error']=self.Error
        return str(dict).replace("'", "\"")


class SysInfo(Message):
    def __init__(self, id, agentId, date):
        mType = MessageType.SYSINFO
        super().__init__(id, agentId, date, mType)

    def set_memory_info(self, total, free, used):
        self.total_memory = total
        self.free_memory = free
        self.used_memory = used

    def set_cpus_used(self, cpu_used):
        self.cpu_used=cpu_used

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
        str = super().to_str()
        str = str + "\ntotal memory:{0} free memory:{1} used memory:{2}\n" \
                    "total disk:{3} free disk:{4} used disk:{5}\n" \
                    "cpu used:{6}\n" \
                    "is peer deployed:{7} is peer started:{8}\n" \
                    "is ca deployed:{9} is ca started:{10}\n" \
                    "is orderer deployed:{11} is orderer started:{12}".format(self.total_memory, self.free_memory, self.used_memory,
                                          self.total_disk, self.free_disk, self.used_disk,
                                          self.cpu_used, self.is_peer_deployed, self.is_peer_started,
                                          self.is_ca_deployed, self.is_ca_started,
                                          self.is_orderer_deployed, self.is_orderer_started)
        return str

class Ack(Message):
    def __init__(self, id, agentId, date):
        mType = MessageType.ACK
        super().__init__(id, agentId, date, mType)

    def set_libelle(self, libelle):
        self.libelle = libelle

    def to_str(self):
        str = super().to_str()
        str = str + "ack:{0} ".format(self.libelle)
        return str

class Error(Message):
    def __init__(self, id, agentId, date):
        mType = MessageType.ERROR
        super().__init__(id, agentId, date, mType)

    def set_error_libelle(self, libelle):
        self.libelle = libelle

    def to_str(self):
        str = super().to_str()
        str = str + "error:{0} ".format(self.libelle)
        return str

class Content(Message):
    def __init__(self, id, agentId, date, body, error):
        mType = MessageType.CONTENT
        super().__init__(id, agentId, date, mType, body, error)
