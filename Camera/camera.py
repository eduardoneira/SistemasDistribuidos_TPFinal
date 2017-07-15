#!/bin/python3

import json
import os
import pika
import logging

def set_logger(logging_level):
  logging.basicConfig(  level=logging_level,
                        format='%(asctime)s %(levelname)-8s Camera   '+ str(os.getpid()) +'    %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='./Camera.log',
                        filemode='w')

  logging.getLogger('pika').setLevel(logging.WARNING)


#  STARTS PROGRAM

print('Configurando camara')

with open('config.json') as config_file:    
  config = json.load(config_file)

set_logger(config['logging_level'])

logging.debug('Creando conexión a servidor CMB en host %s usando la cola %s',config['host'],config['queue'])

connection = pika.BlockingConnection(pika.ConnectionParameters(host=config['host']))
channel = connection.channel()

channel.queue_declare(queue=config['queue'])

print('Configuración terminada. Comenzando envió de mensajes')

channel.basic_publish(exchange='',
                      routing_key=config['queue'],
                      body='Hello World!')

logging.debug("Sent 'Hello World!'")
connection.close()

print('Camera terminada')



  