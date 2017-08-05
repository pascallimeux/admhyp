import socket, sys, logging, platform, inspect, zlib, base64
from subprocess import Popen, PIPE, STDOUT

BUFFER_SIZE=1024
default_params = ('127.0.0.1', 8808)
STOPAGENT="KILL"
VERSION="1.0.0"

def init_logger(agent_id, log_mod):
    logger = logging.getLogger()
    logger.setLevel(log_mod)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(log_mod)
    formatter = logging.Formatter('%(asctime)s - agent({}) - %(message)s'.format(agent_id))
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

class Agent():

    def __init__(self, params, log_mod):
        try:
            self.agent_id = "{0}:{1}".format(params[0], str(params[1]))
            self.logger = init_logger(self.agent_id, log_mod)
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind(params)
        except socket.error as e:
            self.logger.debug ('Error to start Agent:{0} {1}'.format(self.agent_id, e))
            exit (-1)

        self.logger.debug("Start agent:{}".format(self.agent_id))
        self.wait_request()

    def wait_request(self):
        request = ""
        while request.upper() != STOPAGENT:
            self.server.listen(1)
            self.connection, address = self.server.accept()
            self.logger.debug("Connection with client: {}".format(str(address)))
            request = self.connection.recv(BUFFER_SIZE).decode('utf-8')
            if not request:
                break
            self.dispatch_request(request)
        self.stop_agent()

    def dispatch_request(self, request):
        self.logger.debug("Request received: \"{}\"".format(request))
        method, params = self.extract_parameters(request)
        if method.upper() != STOPAGENT:
            try:
                self.logger.debug("execute method: act_{0}({1})".format(method, params))
                if params and params !='':
                    getattr(self, "act_"+method)(params)
                else:
                    getattr(self, "act_" + method)()
            except Exception as e:
                self.logger.error(e)
                self.send_message("No method: {0}({1}) on this agent".format(method, params))

    def extract_parameters(self, request):
        try:
            method = request
            parameters = ""
            if "(" in request and ")" in request and request.index('(') < request.index(')'):
                parameters = (request[request.find("(") + 1:request.find(")")])#.strip().split(',')
                #if args and args[0] != '':
                #    parameters = dict(item.split('=') for item in args)
                method = request[0:request.find("(")]
            return method, parameters
        except Exception as e:
            self.logger.error(e)
            raise Exception ("method parameters failled")

    def act_help(self):
        """ Display this help """
        message = "\n"
        for method_name in dir (Agent):
            if method_name.startswith('act_'):
                meth = getattr(Agent, method_name)
                label = ""
                if hasattr(meth, '__doc__'):
                    label = (getattr(meth, '__doc__'))
                args = str(inspect.signature(meth)).replace("self, ", "").replace("self","")
                method_name = "{0}{1}".format(method_name.replace("act_", ""), args)
                message = message + "(agentid):{0:15} -----> {1:20}\n".format(method_name, label)
        self.logger.debug(message)
        self.send_message(message)

    def act_version(self):
        """ Get agent version """
        self.send_message("agent version:{}".format(VERSION))

    def act_infos(self):
        """ Get system infos """
        message ="platform:{0}\nname:{1}\nsystem:{2}\nrelease:{3}\npython version:{4}".format(platform.system(),
                                                                                           platform.uname(),
                                                                                           platform.machine(),
                                                                                           platform.release(),
                                                                                           platform.python_version())

        self.send_message(message)

    def act_test1(self, val1):
        """ méthode de test"""
        self.send_message(val1)

    def act_kill(self):
        """ Kill the remote agent """
        self.logger.debug("Stop agent")
        self.send_message("agent {} killed!".format(self.agent_id))
        self.connection.close()

    def act_add(self, encoded_method):
        """ Add a method """
        try:
            method = zlib.decompress(base64.b64decode(encoded_method))
            setattr(Agent, "act_" + method.name(), method)
            message = "{} added".format(method.name())
        except Exception as e:
            self.logger.error(e)
            message = "add method failled!"
        return self.send_message(message)


    def act_exec_script(self, python_script):
        """ Execute a Python script """

    def act_exec_cmd(self, cmds):
        """ Execute a Linux command """
        process = Popen(cmds, shell=True, stdout=PIPE, stderr=PIPE)
        output, error = process.communicate()
        output = output.decode('utf-8')
        error = error.decode('utf-8')
        code = process.returncode
        if code != 0:
            message = "command failed: code={0}, error={1}".format(code, error)
            return code
        else:
            message = "output={}".format(output)
        return self.send_message(message)

    def send_message(self, msg):
        self.connection.send(msg.encode('utf-8'))



if __name__== '__main__':
    if len(sys.argv)<2:
        params=default_params
    else:
        params=('127.0.0.1', int(sys.argv[1]))
    Agent(params, logging.DEBUG)
