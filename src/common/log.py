# -*- coding: utf-8 -*-
'''
Created on 28 june 2017
@author: pascal limeux
'''

import os
import logging
#from common.constants import logger_filename
# to display log
log_handler = logging.StreamHandler()

#log_handler = logging.FileHandler(logger_filename)

formatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s]"
                           " [%(filename)s:%(lineno)s %(funcName)20s()]"
                           " - %(message)s")

log_handler.setFormatter(formatter)

LOG_LEVEL = eval("logging." + os.environ.get("LOG_LEVEL", "DEBUG"))
