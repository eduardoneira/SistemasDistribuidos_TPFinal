#!/bin/python3

import json
from time import sleep
from modules.graceful_killer import *
from modules.logger import *
from modules.mock_camera import *
from modules.pika_wrapper import *
from datetime import datetime

print('Configurando camara')

with open('config.json') as config_file:    
  config = json.load(config_file)

set_logger(config['logging_level'])

logging.debug('Creando conexión a servidor CMB en host %s usando la cola %s',config['host'],config['queue'])

#TODO: change client to mqtt
client = PikaWrapper(config['host'],config['queue'])

print('Configuración terminada. Comenzando envió de mensajes')

killer = GracefulKiller()
sleep_time = 1 / config['FPS']
payload = {}

camera = MockCamera()

while True:  
  payload['location'] = config['location']
  payload['timestamp'] = datetime.now().strftime('%d-%m-%Y||%H:%M:%S.%f')
  payload['frame'] = str(camera.get_frame())

  if payload['frame'] != camera.INVALID():
    client.send(json.dumps(payload))

    print('Mensaje de frame enviado')
    logging.debug('Se envió: \'{'+payload['location']+','+payload['timestamp']+'}\'')

  sleep(sleep_time)

  if killer.kill_now:
    break

print('Se recibió una señal de salida, cerrando conexión')

  client.close()

print('Proceso terminado')