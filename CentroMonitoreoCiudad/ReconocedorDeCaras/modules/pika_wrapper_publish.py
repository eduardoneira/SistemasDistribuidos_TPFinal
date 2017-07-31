#!/bin/python3

import pika
import logging

class PikaWrapperPublisher:

  def __init__(self,host,exchange):
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    
    self.channel = self.connection.channel()

    self.channel.exchange_declare(exchange=exchange,
                                  type='direct')

    self.host = host
    self.exchange = exchange

    logging.debug('Se establecio una conexion como publisher con el host: '+ host+' con exchange: '+exchange)

  def send(self,message,routing_key):
    self.channel.basic_publish(exchange=self.exchange,
                               routing_key=routing_key,
                               body=message)

  def sleep(self,time):
    self.connection.sleep(time)

  def close(self):
    self.connection.close()