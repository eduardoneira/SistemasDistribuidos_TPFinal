#!/bin/python3

import json
from modules.graceful_killer import *
from modules.logger import *
from modules.pika_wrapper_subscriber import *
from modules.pika_wrapper_publisher import *
from modules.face_cropper import *

def callback(ch, method, properties, body):
  payload = json.loads(body.decode('utf-8'))
  logging.debug('Mensaje recibido: {%s,%s}', payload['location'],payload['timestamp'])
  print("Se recibio mensaje de frame. Comienza el cropeo")

  payload['type'] = 'CMB_feed'
  payload['faces'] = []
  for img in cropper.crop_base_64(payload['frame']):
    payload['faces'].append(img)
  
  if len(payload['faces']) > 0:
    client.send(json.dumps(payload))
    logging.debug('Se encontraron %d caras, enviando mensaje a CMC con %s, %s',len(payload['faces']),payload['location'],payload['timestamp'])
    print('Se envio al CMC la foto con las caras encontradas')
  else:
    logging.debug('No se encontraron caras en la foto con %s, %s',payload['location'],payload['timestamp'])
    print('No se encontraron caras luego de cropear')

if __name__ == '__main__':
  print('Configurando CMB')

  with open('config.json') as config_file:
    config = json.load(config_file)

  set_logger(config['logging_level'])

  server = PikaWrapperSubscriber( host=config['host_camera'],
                                  topic=config['topic_camera'],
                                  queue=config['queue'],
                                  routing_key=config['routing_key_camera'])

  client = PikaWrapperPublisher(host=config['host_cmc'],
                                topic=config['topic_cmc'])

  cropper = FaceCropper()

  killer = GracefulKiller()
  killer.add_connection(server)

  server.set_receive_callback(callback)

  print('[*] Esperando mensajes para procesar. Para salir usar CTRL+C')
  server.start_consuming()