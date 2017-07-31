#!/bin/python3

import pika
import logging

class PikaWrapperReceiver:

  def __init__(self,host,queue):
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))

    self.channel = self.connection.channel()

    self.channel.queue_declare( queue=queue,
                                exclusive=True)

    self.host = host
    self.queue = queue

    logging.debug('Se establecio una conexion para recibir mensajes con el host: '+ host+' y escuchando de la cola: '+ queue)

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
