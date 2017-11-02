#!/bin/python3

import pika
import logging

class PikaWrapperSubscriber:

  def __init__(self,host,topic,queue,routing_key):
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    
    self.channel = self.connection.channel()

    self.channel.queue_declare( queue=queue,
                                exclusive=True)

    self.channel.queue_bind(exchange=topic,
                            queue=queue,
                            routing_key=routing_key)  

    self.host = host
    self.queue = queue
    self.topic = topic
    self.routing_key = routing_key

    logging.debug('Se establecio una conexion como subscriber con el host: '+ host+' con topic: '+topic+', escuchando de la cola: '+queue+' con routing key: '+routing_key)

  def handle_message(self,ch, method, properties, body):
    return self.handle_message_callback(body)

  def set_receive_callback(self,callback):
    self.handle_message_callback = callback
    self.tag = self.channel.basic_consume(self.handle_message,
                                          queue=self.queue,
                                          no_ack=True)
    return self.tag

  def start_consuming(self):
    self.channel.start_consuming()

  def close(self):
    try:
      self.channel.basic_cancel(self.tag)
      self.channel.stop_consuming()
      self.connection.close()
    except pika.exceptions.ConnectionClosed:
      logging.warning('Ya se habia cerrado la conexion')
