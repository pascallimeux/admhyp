# -*- coding: utf-8 -*-
'''
Created on 22 june 2017
@author: pascal limeux
'''

#from serverManager import ServerManager
#from rcmd import CreateRemoteAdmin
#from server import Server
#from lcmd import SetupHyperledger


import argparse
parser = argparse.ArgumentParser(description='description')
parser.add_argument('-p', '--port', type=int, help='port to expose API', required=False)
from config import appconf, ROOT_DIR
from app.common.lcmds import get_local_ipaddress
from app import app

from app.common.log import get_logger
logger = get_logger()

def user_is_logged_in():
    return True


if __name__ == "__main__":
    try:
        args = parser.parse_args()
        port = args.port
        if port == None:
            port=app.config['PORT']
        host = app.config['HOST']
        if host == None:
            host = get_local_ipaddress()
        logger.info("Start application in {0} mode, hostname:{1}:{2}".format(appconf().APPMODE, host, port))
        app.run(host=host, port=port, debug=app.config['DEBUG'])
        peerHostname    = '192.168.0.106'
        caHostname      = '192.168.0.104'
        ordererHostname = '192.168.0.108'
    finally:
        logger.info("Stop application...")

#    try:
        #SetupHyperledger()
        #CreateRemoteAdmin(hostname=peerHostname, username=username, password=password, pub_key_file=pub_key_file)
        #CreateRemoteAdmin(hostname=caHostname, username=username, password=password, pub_key_file=pub_key_file)
        #CreateRemoteAdmin(hostname=ordererHostname, username=username, password=password, pub_key_file=pub_key_file)
        #print (logger_filename)
        #srvManager = ServerManager()
        #peer       = srvManager.CreatePeer(hostname=peerHostname, key_file=key_file)
        #print("----------------------------")
        #ca         = srvManager.CreateCA(hostname=caHostname,      key_file=key_file)
        #print("----------------------------")
        #orderer    = srvManager.CreateOrderer(hostname=ordererHostname, key_file=key_file)
        #print("----------------------------")
        #print (peer)
        #print (ca)
        #print (orderer)
        #ca.UpdateSystem()
        #ca.CreateHyperledgerFolders()
        #ca.GetBinaries()
        #ca.SendLogs()
        #server.TransfertBinaries()
#    except Exception as e:
#        logger.error(e)
