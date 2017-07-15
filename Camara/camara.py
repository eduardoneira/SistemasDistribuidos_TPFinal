#!/bin/python3

import json
import signal, os
from time import sleep
import pika
import logging

#TODO: Modularizar a archivos
def set_logger(logging_level):
  logging.basicConfig(  level=logging_level,
                        format='%(asctime)s %(levelname)-8s Camera   '+ str(os.getpid()) +'    %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='./log/Camara.log',
                        filemode='w')

  logging.getLogger('pika').setLevel(logging.WARNING)

class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self,signum, frame):
    self.kill_now = True
    logging.debug('Llego señal de salida. Se va a terminar la captura de fotos')


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

killer = GracefulKiller()
sleep_time = 1 / config['FPS']

while True:
  

  channel.basic_publish(exchange='',
                        routing_key=config['queue'],
                        body='Hello World!')
  print('Mensaje enviado')
  logging.debug('Se envió: \'Hello World!\'')

  sleep(sleep_time)

  if killer.kill_now:
    break

print('Se recibió una señal de salida, cerrando conexión')

connection.close()

print('Proceso terminado')