# -*- coding: utf-8 -*-
'''
Created on 22 june 2017
@author: pascal limeux
'''

import argparse
parser = argparse.ArgumentParser(description='description')
parser.add_argument('-p', '--port', type=int, help='port to expose API', required=False)
from config import appconf
from app.agent.agentManager import AgentManager
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
        agent_manager = AgentManager()
        logger.info("\n --------------------\n Start application in {0} mode\n * hostname: {1}:{2}\n * boker:    {3}:{4}\n --------------------\n".format(appconf().APPMODE, host, port, appconf().BROKERIP,  appconf().BROKERPORT))
        app.run(host=host, port=port, debug=app.config['DEBUG'])
    finally:
        agent_manager.stop_listener()
        logger.info("Stop application...")
