#!/bin/python3

import pika
import json
import logging

class FaceRecognizerClient(object):
  def __init__(self,host,queue_send,queue_receive):
    self.queue_send = queue_send
    self.queue_receive = queue_receive
    self.host = host

    self.__connect()

  def __connect(self):
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))

    self.channel = self.connection.channel()

    self.channel.queue_declare( queue=self.queue_receive)

    self.channel.basic_consume(self.on_response,
                               no_ack=True,
                               queue=self.queue_receive)

  def on_response(self, ch, method, props, body):
    self.response = body

  def publish(self, message):
    self.response = None
    try:
      self.__publish(message)
    except pika.exceptions.ConnectionClosed:
      logging.warning('Se perdio la conexion, volviendo a conectarse')
      self.__connect()
      self.__publish(message)

    logging.debug('Se envio mensaje al face recognizer. Esperando su respuesta')
    while self.response is None:
        self.connection.process_data_events()

    logging.debug('El face recognizer respondio %s',self.response)

    return self.response

  def __publish(self,message):
    self.channel.basic_publish(exchange='',
                           routing_key=self.queue_send,
                           properties=pika.BasicProperties(
                                         reply_to = self.queue_receive
                                      ),
                           body=message)

  def update(self,images):
    message = {
                'type': 'update',
                'images': images
              }

    response = json.loads(self.publish(json.dumps(message)).decode('utf-8'))
    return response['id']

  def predict(self,faces):
    message = {
            'type': 'predict',
            'faces': faces
          }

    response = json.loads(self.publish(json.dumps(message)).decode('utf-8'))
    return response['ids']

  def close(self):
      try:
        self.connection.close()
      except pika.exceptions.ConnectionClosed:
        logging.warning('La conexion ya estaba cerrada')
