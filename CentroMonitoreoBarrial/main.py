#!/usr/bin/python3

import json
from modules.graceful_killer import *
from modules.logger import *
from modules.pika_wrapper_subscriber import *
from modules.pika_wrapper_publisher import *
from modules.face_cropper import *

def handle_message(body):
  payload = json.loads(body.decode('utf-8'))
  logging.debug('Mensaje recibido: {%s,%s}', payload['location'],payload['timestamp'])
  print("Se recibio mensaje de frame. Comienza el cropeo")

  payload['faces'] = cropper.crop_base64(payload['frame'])
  
  if config['logger']['save_image']:
    save_image_b64(payload['frame'],payload['faces'])

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

  set_logger(config['logger']['level'])
  if config['logger']['save_image']:
    set_image_directory()

  cropper = FaceCropper(config['face_cropper'])

  client = PikaWrapperPublisher(host=config["network"]['cmc_host'],
                                topic=config["network"]['topic_cmc'])

  server = PikaWrapperSubscriber( host=config["network"]['camera_host'],
                                  topic=config["network"]['topic_camera'],
                                  routing_key=config["network"]['routing_key_camera'],
                                  queue=config["network"]['queue'])
  
  server.set_receive_callback(handle_message)
  
  killer = GracefulKiller()
  killer.add_connection(client)
  killer.add_connection(server)

  print('[*] Esperando mensajes para procesar. Para salir usar CTRL+C')
  server.start_consuming()