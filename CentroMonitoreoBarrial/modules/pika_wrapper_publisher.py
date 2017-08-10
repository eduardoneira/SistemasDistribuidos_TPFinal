#!/bin/python3

import pika
import logging

class PikaWrapperPublisher:

  def __init__(self,host,topic):
    self.host = host
    self.topic = topic

    self.__connect()

    logging.debug('Se establecio una conexion como publisher con el host: '+host+' con topic: '+topic)

  def __connect(self):
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
    
    self.channel = self.connection.channel()

    self.channel.exchange_declare(exchange=self.topic,
                                  type='topic')

  def send(self,message):
    try: 
      self.__publish(message)
    except pika.exceptions.ConnectionClosed:
      logging.warning('Se perdio la conexion, volviendo a conectarse')
      self.__connect()
      self.__publish(message)

  def __publish(self,message):
    self.channel.basic_publish(exchange=self.topic,
                           routing_key='',
                           body=message)

  def sleep(self,time):
    self.connection.sleep(time)

  def close(self):
    try:
      self.connection.close()
    except pika.exceptions.ConnectionClosed:
      logging.warning('Ya se habia cerrado la conexion')