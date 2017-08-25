# -*- coding: utf-8 -*-
'''
Created on 22 june 2017
@author: pascal limeux
'''


from subprocess import Popen, PIPE, STDOUT
import platform
from app.common.log import get_logger

logger = get_logger()

def get_plateform():
    print ("platform:{0}\nname:{1}\nsystem:{2}\nrelease:{3}\npython version:{4}".format(platform.system(), platform.uname(), platform.machine(), platform.release(), platform.python_version()))

def exec_local_cmd2(cmd):
    try:
        logger.debug("Execute locale command:{}".format(cmd))
        process = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
        for line in process.stdout:
            print (line.decode('utf-8'))
        process.wait()
    except Exception as e:
        logger.error (e)


#example "df -k && ls -lisa"
def exec_local_cmd(cmds):
    logger.debug("Exec local cmd: {}".format(cmds))
    process = Popen(cmds, shell=True, stdout=PIPE, stderr=PIPE)
    output, error = process.communicate()
    output = output.decode('utf-8')
    error = error.decode('utf-8')
    code = process.returncode
    if code != 0:
        logger.error ("command failed: code={0}, error={1}".format(code, error))
        return code
    logger.debug ("output={}".format(output))
    return code

#example ("df -k", "ls -lisa", "ls /out")
def exec_cmd_one_by_one(*args):
    for cmd in args:
        process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        output, error = process.communicate()
        output = output.decode('utf-8')
        error = error.decode('utf-8')
        code = process.returncode
        if code != 0:
            logger.error ("command failed: code={0}, error={1}".format(code, error))
            return code
        logger.debug ("output={}".format(output))
    return code

def get_external_ipaddress():
    import urllib.request
    extipaddr = urllib.request.urlopen('http://ident.me').read().decode('utf8')
    return extipaddr

def get_local_ipaddress():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 0))
    ipaddr=s.getsockname()[0]
    return (ipaddr)

