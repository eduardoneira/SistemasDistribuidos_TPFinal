#!/bin/python3

import json
from modules.graceful_killer import *
from modules.logger import *
from modules.mock_camera import *
from modules.mqtt_wrapper import *
from datetime import datetime
from time import sleep
import pdb
import base64

print('Configurando camara')

with open('config.json') as config_file:    
  config = json.load(config_file)

set_logger(config['logging_level'])

logging.debug('Creando conexión a servidor CMB en host: %s usando topic: %s',config['host'],config['topic'])

client = MqttWrapper(config['host'])

print('Configuración terminada. Comenzando envió de mensajes')

sleep_time = 1 / config['FPS']
payload = {}

if config['camera'] == "mock": 
  camera = MockCamera() 
elif config['camera'] == "rasppi":
  from modules.rasp_camera import *
  camera = RaspCamera()

killer = GracefulKiller()

while True:  
  payload['location'] = config['location']
  payload['timestamp'] = datetime.now().strftime('%d-%m-%Y||%H:%M:%S.%f')
  payload['frame'] = camera.get_frame()

  if payload['frame'] != camera.INVALID():
    payload['frame'] = payload['frame'].decode('utf-8')
    
    client.send(config['topic'],json.dumps(payload))

    print('Mensaje de frame enviado')
    logging.debug('Se envió: \'{'+str(payload['location'])+','+payload['timestamp']+'}\'')

  sleep(sleep_time)

  if killer.kill_now:
    break

print('Se recibió una señal de salida, cerrando conexión')

client.close()

print('Proceso terminado')