from enum import Enum
from app.common.log import get_logger
logger = get_logger()

class CreateMessageException(Exception):
    pass

class OrderType(Enum):
    STOPAGENT         = 0
    DEPLOYCA          = 1
    STARTCA           = 2
    ISCASTARTED       = 3
    ISCADEPLOYED      = 4
    STOPCA            = 5
    DEPLOYPEER        = 6
    STARTPEER         = 7
    ISPEERSTARTED     = 8
    ISPEERDEPLOYED    = 9
    STOPPEER          = 10
    DEPLOYORDERER     = 11
    STARTORDERER      = 12
    ISORDERERSTARTED  = 13
    ISORDERERDEPLOYED = 14
    STOPORDERER       = 15
    INITENV           = 16
    REMOVEENV         = 17
    REGISTERUSER      = 18
    REGISTERNODE      = 19
    REGISTERADMIN     = 20
    ENROLLUSER        = 21
    ENROLLNODE        = 22
    ENROLLADMIN       = 23

STATUSTOPIC   = "status/"         # status / clientID           Agent   ---> SysInfo_dto    --->    Manager
ORDERTOPIC    = "orders/"         # orders / clientID           Manager ---> Order_dto      --->    Agent
RESPONSETOPIC = "responses/"      # responses / messageID       Agent   ---> Response_dto   --->    Manager

class Message_dto ():
    def __init__(self, id, agentId, date):
        self.messageId = id
        self.agentId = agentId
        self.created = date

    def to_str(self):
        return "MessageId={0}, AgentId={1}, Created={2} ".format(self.messageId, self.agentId, self.created)

    def to_json(self):
        dict = {}
        dict['messageid']=self.messageId
        dict['agentid']=self.agentId
        dict['created']=str(self.created)
        return str(dict).replace("'", "\"")

class Order_dto(Message_dto):
    def __init__(self, id, agentId, date, order, args):
        super().__init__(id, agentId, date)
        self.order=order
        self.args=args

    def to_str(self):
        str = super().to_str()
        str = str + " order:{0}".format(self.order)
        return str

    def to_json(self):
        dict = {}
        dict['messageid']=self.messageId
        dict['agentid']=self.agentId
        dict['created']=str(self.created)
        dict['order']=self.order.value
        if len(self.args)>0:
            dict['args']=self.args
        return str(dict).replace("'", "\"")


class Response_dto(Message_dto):
    def __init__(self, id, agentId, date, order, error, response, content):
        super().__init__(id, agentId, date)
        self.order=order
        self.error=error
        self.response=response
        self.content=content

    def to_str(self):
        str = super().to_str()
        str = str + " order:{0} ,response:{1}".format(self.order, self.response)
        return str


class SysInfo_dto(Message_dto):
    def __init__(self, id, agentId, date):
        super().__init__(id, agentId, date)

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
