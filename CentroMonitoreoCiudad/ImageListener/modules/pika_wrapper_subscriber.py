#!/bin/python3

import pika
import logging

class PikaWrapperSubscriber:

  def __init__(self,host,topic):
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))

    self.channel = self.connection.channel()

    self.channel.exchange_declare(exchange=topic,
                                  type='topic')

    result = self.channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    self.channel.queue_bind(exchange=topic,
                            queue=queue_name,
                            routing_key='#')

    self.host = host
    self.queue = queue_name
    self.topic = topic

    logging.debug('Se establecio una conexion como subscriber con el host: '+ host+' con topic: '+topic+' y escuchando de la cola: '+ queue_name)

  def set_receive_callback(self,callback):
    self.tag = self.channel.basic_consume(callback,
                                          queue=self.queue,
                                          no_ack=True)
    return self.tag

  def start_consuming(self):
    self.channel.start_consuming()

  def close(self):
    try:
      self.channel.basic_cancel(self.tag)
      self.channel.stop_consuming()
    finally:
      try:
        self.connection.close()
      except pika.exceptions.ConnectionClosed:
        logging.warning('La conexion ya estaba cerrada')
