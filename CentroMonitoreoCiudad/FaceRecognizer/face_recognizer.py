#!/bin/python3

import json
from modules.LBPH_wrapper import *
from modules.pika_wrapper_receive import *
from modules.logger import *
from modules.graceful_killer import *

def handle_message():
  request = json.load(body)
  response = {}

  if request['type'] == config['request_update']:
    id = face_recognizer.update_base64(request['image'])
    response['id'] = id
  elif request['type'] == config['request_predict']:
    ids = []
    for img in request['faces']:
      ids.append(face_recognizer.predict_base64(img))
    response['ids'] = ids

  return json.dumps(response)
  

if __name__ == '__main__':
  print('Configurando face recognizer.')

  with open('config.json') as config_file:
    config = json.load(config_file)

  set_logger(config['stem_name_log'],config['logging_level'])

  graceful_killer = GracefulKiller()

  face_recognizer = LBPHWrapper(config['MIN_MATCH_PROBABILITY'],
                                config['MIN_UPDATE_PROBABILITY'])

  server = PikaWrapperReceiver('localhost',config['queue_request'])
  server.set_receive_callback(handle_message)

  graceful_killer.add_predictor(face_recognizer)
  graceful_killer.add_connection(server)

  print('Configuracion terminada. Esperando mensajes.')
  server.start_consuming()