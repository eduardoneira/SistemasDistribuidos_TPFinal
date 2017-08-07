#!/bin/python3

import pika
import uuid
import logging

class RpcClient(object):
  def __init__(self,host,queue_rpc):
    self.host = host
    self.queue_rpc = queue_rpc

    self.__connect()

  def __connect(self):
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))

    self.channel = self.connection.channel()

    result = self.channel.queue_declare(exclusive=True)
    self.callback_queue = result.method.queue

    self.channel.basic_consume(self.on_response,
                               no_ack=True,
                               queue=self.callback_queue)
    

  def on_response(self, ch, method, props, body):
    if self.corr_id == props.correlation_id:
        self.response = body

  def call(self, message):
    self.response = None
    self.corr_id = str(uuid.uuid4())

    try:
      self.__publish(message)
    except pika.exceptions.ConnectionClosed:
      logging.warning('Se perdio la conexion, volviendo a conectarse')
      self.__connect()
      self.__publish(message) 

    logging.debug('Se envio un mensaje rpc al server CMC')
    while self.response is None:
        self.connection.process_data_events()

    logging.debug('Se recibio la respuesta del server CMC')
    return self.response

  def __publish(self,message):
    self.channel.basic_publish(exchange='',
                             routing_key=self.queue_rpc,
                             properties=pika.BasicProperties(
                                   reply_to = self.callback_queue,
                                   correlation_id = self.corr_id,
                                   ),
                             body=message)

  def close(self):
    self.connection.close()
