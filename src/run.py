# -*- coding: utf-8 -*-
'''
Created on 22 june 2017
@author: pascal limeux
'''

#from serverManager import ServerManager
#from rcmd import CreateRemoteAdmin
#from server import Server
#from lcmd import SetupHyperledger


from config import appconf
from app import app

from common.log import get_logger
logger = get_logger()

def user_is_logged_in():
    return True


if __name__ == "__main__":
    try:
        logger.info("Start application in {} mode".format(appconf().APPMODE))
        app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
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
