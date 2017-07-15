#!/bin/python3

import logging
import os

def set_logger(logging_level):
  logging.basicConfig(  level=logging_level,
                        format='%(asctime)s %(levelname)-8s Camera   '+ str(os.getpid()) +'    %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='./log/Camara.log',
                        filemode='w')

  logging.getLogger('pika').setLevel(logging.WARNING)