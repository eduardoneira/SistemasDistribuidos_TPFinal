#!/bin/python3

import pika
import logging

class PikaWrapperSubscriber:

  def __init__(self,host,topic,queue):
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    
    self.channel = self.connection.channel()

    self.channel.queue_declare( queue=queue,
                                exclusive=True)

    self.channel.queue_bind(exchange=topic,
                            queue=queue,
                            routing_key='#')  

    self.host = host
    self.queue = queue
    self.topic = topic

    logging.debug('Se establecio una conexion como subscriber con el host: '+ host+' con topic: '+topic+' y escuchando de la cola: '+queue)

  def set_receive_callback(self,callback):
    self.tag = self.channel.basic_consume(callback,
                                          queue=self.queue,
                                          no_ack=True)
    return self.tag

  def start_consuming(self):
    self.channel.start_consuming()

  def close(self):
    self.channel.basic_cancel(self.tag)
    self.channel.stop_consuming()
    self.connection.close()