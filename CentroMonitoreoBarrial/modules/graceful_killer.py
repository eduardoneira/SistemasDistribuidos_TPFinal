#!/bin/python3

import signal
import logging
import pika

class GracefulKiller:
  __channel = None
  __queues = []

  def __init__(self,channel):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)
    self.__channel = channel

  def add_queue(self,queue):
    self.__queues.append(queue)

  def exit_gracefully(self,signum,frame):
    logging.debug('Llego señal de salida. Se va a cerrar el CMB')
    
    for queue in self.__queues:
      self.__channel.basic_cancel(queue)
    
    self.__channel.stop_consuming()
    exit()