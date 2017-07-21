# -*- coding: utf-8 -*-
'''
Created on 22 june 2017
@author: pascal limeux
'''


from subprocess import Popen, PIPE, STDOUT

from app.common.log import get_logger

logger = get_logger()

def exec_local_cmd(cmd):
    try:
        #cmd = cmd.strip(" ")
        logger.debug("Execute locale command:{}".format(cmd))
        process = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
        for line in process.stdout:
            print (line.decode('utf-8'))
        process.wait()
    except Exception as e:
        logger.error (e)

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