#!/bin/python3

import logging
import glob
import os
def set_logger(logging_level):

  #Para no sobreescribir
  id = len(glob.glob("./ProcesadorDeImagenes/log/*.log")) +1

  logging.basicConfig(  level=logging_level,
                        format='%(asctime)s %(levelname)-8s Camera   '+ str(os.getpid()) +'    %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='./ProcesadorDeImagenes/log/HTTP_query_handler'+str(id)+'.log',
                        filemode='w')

  logging.getLogger('pika').setLevel(logging.WARNING)
