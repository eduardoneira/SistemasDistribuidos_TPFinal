#!/bin/python3

import logging
import glob
import os

def set_logger(logging_level):  
  if not os.path.exists('./log/'):
    os.makedirs('./log/')

  #Para no sobreescribir
  id = len(glob.glob("./log/ImageListener*.log")) +1

  logging.basicConfig(  level=logging_level,
                        format='%(asctime)s %(levelname)-8s IMAGE    '+ str(os.getpid()) +'    %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='./log/ImageListener'+str(id)+'.log',
                        filemode='w')

  logging.getLogger('pika').setLevel(logging.WARNING)
