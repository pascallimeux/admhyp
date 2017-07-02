# -*- coding: utf-8 -*-
'''
Created on 28 june 2017
@author: pascal limeux
'''

import os, logging

# to display log
log_handler = logging.StreamHandler()

#import config
#log_handler = logging.FileHandler(config.LOGFILENAME)

formatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s]"
                           " [%(filename)s:%(lineno)s %(funcName)20s()]"
                           " - %(message)s")

log_handler.setFormatter(formatter)

LOG_LEVEL = eval("logging." + os.environ.get("LOG_LEVEL", "DEBUG"))
