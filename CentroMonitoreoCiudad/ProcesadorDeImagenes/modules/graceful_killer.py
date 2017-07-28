#!/bin/python3

import signal
import logging
import pika

class GracefulKiller:
  __connections = []
  __predictors = []
  
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)
    
  def add_connection(self,connection):
    self.__connections.append(connection)

  def add_predictor(self,predictor):
    self.__predictors.append(predictor)

  def exit_gracefully(self,signum,frame):
    logging.debug('Llego señal de salida. Se va a cerrar el CMB')    

    for connection in self.__connections:
      connection.close()

    for predictor in self.__predictors:
      predictor.save()

    exit()