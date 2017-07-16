#!/bin/python3

import json
from time import sleep
from modules.graceful_killer import *
from modules.logger import *
import pika

print('Configurando camara')

with open('config.json') as config_file:    
  config = json.load(config_file)

set_logger(config['logging_level'])

logging.debug('Creando conexión a servidor CMB en host %s usando la cola %s',config['host'],config['queue'])

connection = pika.BlockingConnection(pika.ConnectionParameters(host=config['host']))
channel = connection.channel()

channel.queue_declare(queue=config['queue'])

print('Configuración terminada. Comenzando envió de mensajes')

killer = GracefulKiller()
sleep_time = 1 / config['FPS']

while True:  

  channel.basic_publish(  exchange='',
                          routing_key=config['queue'],
                          body='Hello World! ')
  print('Mensaje enviado')
  logging.debug('Se envió: \'Hello World!\'')

  i += 1
  sleep(sleep_time)

  if killer.kill_now:
    break

print('Se recibió una señal de salida, cerrando conexión')

connection.close()

print('Proceso terminado')