#!/bin/python3

import pika

class PikaWrapper:

  def __init__(self,host,topic,queue):
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    
    self.channel = self.connection.channel()

    self.channel.exchange_declare( exchange=topic,
                                   type='topic')
    self.queue = queue
    self.host = host
    self.topic = topic
    
  def send(self,message):
    self.channel.basic_publish(exchange=self.topic,
                               routing_key=self.queue,
                               body=message)

  def sleep(self,time):
    self.connection.sleep(time)

  def close(self):
    self.connection.close()


