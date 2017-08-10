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

  def template_callback(self,ch,method, props, body):
    response = self.callback(body)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     body=str(response))

    ch.basic_ack(delivery_tag = method.delivery_tag)

  def set_receive_callback(self,callback):
    self.callback = callback

    self.tag = self.channel.basic_consume(self.template_callback,
                                          queue=self.queue)
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

