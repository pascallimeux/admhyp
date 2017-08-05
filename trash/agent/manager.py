import socket, sys, logging, string, base64, zlib

RED   = "\033[1;31m"
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

BUFFER_SIZE=1024
STOPMNG = "STOP"

def init_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

logger=init_logger()
agents = []

def init_agents():
    agents.append(('127.0.0.1', 8808))
    agents.append(('127.0.0.1', 8809))
    agents.append(('127.0.0.1', 8810))

def send(agent_nb, method):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(agents[agent_nb])
        s.send("{}".format(method).encode())
        result = s.recv(BUFFER_SIZE)
        print('Received > {}'.format(result.decode("utf-8")))

def new_method1(self):
    """ Add a new method1 """

def send_new_method(agent_nb, method):
    encoded = base64.b64encode(zlib.compress(method))
    method="add({})".format(encoded)
    send(agent_nb, method)


if __name__== '__main__':
    init_agents()
    message = ""
    while STOPMNG not in message:
        try:
            message = input('Message  > ')
            if "RIRI" in message:
                send_new_method(0, new_method1)
                break
            if STOPMNG in message:
                break
            messages = message.split(':')
            if len(messages) == 2:
                agent_nb = int (messages [0])
                method = message[message.find(":")+ 1:]
            else:
                agent_nb = 0
                method=message
            logger.debug("agent={0} method={1}".format(str(agent_nb), method))
            send(agent_nb =agent_nb, method=method)
        except ConnectionRefusedError :
            sys.stdout.write(RED)
            print ("no connection with this agent: {}".format(agents[agent_nb]))
            sys.stdout.write(RESET)
        except Exception as e:
            print (e)
            sys.stdout.write(RED)
            print ("Invalid request format !")
            sys.stdout.write(RESET)
