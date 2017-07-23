#!/bin/python3

import pika

class PikaWrapper:

  def __init__(self,host,queue):
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    
    self.channel = connection.channel()
    self.host = host
    self.queue = queue
    self.channel.queue_declare(queue=queue)

  def send(self,message):
    channel.basic_publish(exchange='',
                          routing_key=self.queue,
                          body=message)

  def close(self):
    self.connection.close()


