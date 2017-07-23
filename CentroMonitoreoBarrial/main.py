#!/bin/python3

import json
from modules.graceful_killer import *
from modules.logger import *
import pika

print('Configurando CMB')

with open('config.json') as config_file:    
  config = json.load(config_file)

set_logger(config['logging_level'])

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
logging.debug('Se creo una conexion a rabbitmq broker en localhost')
channel = connection.channel()

channel.exchange_declare(exchange=config['topic'],
                         type='topic')

killer = GracefulKiller(channel)

result = channel.queue_declare(exclusive=True)

queue_name = result.method.queue
logging.debug('Se va a escuchar de la cola: '+ queue_name)

channel.queue_bind(exchange=config['topic'],
                   queue=queue_name,
                   routing_key='#')


def callback(ch, method, properties, body):
  #TODO: OPENCV AND RESEND
  logging.debug('Message received: %s', body)
  print(" [x] Received %r" % body)

tag = channel.basic_consume(callback,
                            queue=queue_name,
                            no_ack=True)

killer.add_queue(tag)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()