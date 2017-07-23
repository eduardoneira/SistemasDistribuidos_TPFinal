#!/bin/python3

import json
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

client = PikaWrapper(config['host'],config['topic'],config['queue'])

print('Configuración terminada. Comenzando envió de mensajes')

sleep_time = 1 / config['FPS']
payload = {}

camera = MockCamera()
killer = GracefulKiller()

while True:  
  payload['location'] = config['location']
  payload['timestamp'] = datetime.now().strftime('%d-%m-%Y||%H:%M:%S.%f')
  payload['frame'] = str(camera.get_frame())

  if payload['frame'] != camera.INVALID():
    client.send(json.dumps(payload))

    print('Mensaje de frame enviado')
    logging.debug('Se envió: \'{'+str(payload['location'])+','+payload['timestamp']+'}\'')

  client.sleep(sleep_time)

  if killer.kill_now:
    break

print('Se recibió una señal de salida, cerrando conexión')

client.close()

print('Proceso terminado')