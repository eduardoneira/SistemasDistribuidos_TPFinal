#!/bin/python3

import logging
import glob
import os

PROCESS_NAME = "IMAGE_LISTENER"

def set_logger(logging_level):  
  if not os.path.exists('./log/'):
    os.makedirs('./log/')

  logging.basicConfig(  level=logging_level,
                        format='%(asctime)s %(levelname)-8s IMAGE    '+ str(os.getpid()) +'    %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='./log/'+PROCESS_NAME+'.log',
                        filemode='w')

  logging.getLogger('pika').setLevel(logging.WARNING)
