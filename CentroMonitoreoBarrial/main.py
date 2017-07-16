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
channel = connection.channel()

killer = GracefulKiller(channel)

channel.queue_declare(queue=config['queue_camara'])

def callback(ch, method, properties, body):
  #TODO: OPENCV
  logging.debug('Message received: %s', body)
  print(" [x] Received %r" % body)

tag = channel.basic_consume(callback,
                            queue=config['queue_camara'],
                            no_ack=True)

killer.add_queue(tag)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()