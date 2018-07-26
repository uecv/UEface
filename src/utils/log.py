#!/usr/bin/env python 
# coding: utf-8 
""" 
   @author: kenwood
   @time: 18-6-20 上午9:56  
"""
import logging

import Constant
from src.Config import Config

conf = Config.Config(Constant.CONFIG_PATH)


LOG_LEVEL = conf.get('log', 'log_level')
LOG_DIR = conf.get('log','log_dir')
# LOG_LEVEL = 'debug'
# LOG_DIR = './logs'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

def log(name='UEface'):
    logger = logging.getLogger(name)
    logger.setLevel({
                    'DEBUG': logging.DEBUG,
                    'INFO': logging.INFO,
                    }.get(LOG_LEVEL.upper(), 'DEBUG'))
    fh = logging.FileHandler(LOG_DIR)
    fh.setFormatter(logging.Formatter(LOG_FORMAT))
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger

# if __name__ == '__main__':
#     LOG = log()
#     LOG.info('info')
#     LOG.debug('debug')
#     LOG.error('error')
