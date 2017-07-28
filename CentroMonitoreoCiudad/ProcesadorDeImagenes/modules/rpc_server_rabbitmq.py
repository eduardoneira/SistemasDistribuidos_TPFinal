#!/bin/python3 

import pika
import logging
import uuid

class RPCServer:

  PREFETCH_COUNT = 1

  def __init__(self,host,queue,request_callback_main,database,recognizer):
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))

    self.channel = self.connection.channel()

    self.request_callback_main = request_callback_main

    self.channel.queue_declare(queue=queue)

    self.channel.basic_qos(self.PREFETCH_COUNT)
    self.channel.basic_consume(request_callback, queue=queue)

    self.database = database
    self.recognizer = recognizer

    logging.debug('Inicializando rpc server en host %s escuchando de la cola %s',host,queue)

  def request_callback(self,ch, method, props, body):    
    response = self.request_callback_main(body,database,recognizer)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))

    ch.basic_ack(delivery_tag = method.delivery_tag)

  def start():
    logging.debug('Comenzando server rpc. Esperando request RPC')
    self.channel.start_consuming() 