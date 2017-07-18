# -*- coding: utf-8 -*-
'''
Created on 22 june 2017
@author: pascal limeux
'''


from subprocess import Popen, call, PIPE, STDOUT
from common.log import get_logger
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