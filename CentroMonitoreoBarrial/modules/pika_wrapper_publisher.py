#!/bin/python3

import pika
import logging

class PikaWrapperPublisher:

  def __init__(self,host,topic):
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    
    self.channel = self.connection.channel()

    channel.exchange_declare(exchange=topic,
                             type='topic')

    self.host = host
    self.topic = topic

    logging.debug('Se establecio una conexion como publisher con el host: '+ host+' con topic: '+topic)

  def send(self,message):
    self.channel.basic_publish(exchange=self.topic,
                               routing_key='',
                               body=message)

  def sleep(self,time):
    self.connection.sleep(time)

  def close(self):
    self.connection.close()