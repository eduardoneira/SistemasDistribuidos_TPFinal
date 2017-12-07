#!/usr/bin/python3

import json
from modules.logger import *
from modules.graceful_killer import *
from modules.pika_wrapper_subscriber import *
from modules.db_wrapper import *
from modules.file_manager import *
from modules.matcher_wrapper import *

def callback(body):
  payload = json.loads(body.decode('utf-8'))
  logging.debug('Mensaje recibido: %d caras, con %s, %s',len(payload['faces']),payload['location'],payload['timestamp'])

  ids = db.most_wanted_people()
  matches_data = []

  for face in payload['faces']:  
    person_id = matcher.find_match(face, ids)
    if (person_id):
      matches_data.append([person_id, face])
      logging.debug('Se encontro un match con '+person_id+'. Guardando en sistema')
    else:
      logging.debug('No se encontro un match. Descartando')

  if (len(matches_data) > 0):
    big_pic_id = file_manager.save_bigpic_base64(payload['frame'])
    db.save_match_big_pic(big_pic_id, payload['location'][0], payload['location'][1], payload['timestamp'])
    
    for match in matches_data:
      file_manager.save_person_base64(match[0], match[1])
      db.save_match_person(match[0],big_pic_id)

if __name__ == '__main__':
  print('Configurando Worker Image Listener')

  with open('./config.json') as config_file:
    config = json.load(config_file)

  set_logger(config['logger']['logging_level'])
  
  db = DBWrapper(config['db'])

  server = PikaWrapperSubscriber( host=config['network']['broker_cmb_host'],
                                  topic=config['network']['topic_cmc'])
  server.set_receive_callback(callback)

  graceful_killer = GracefulKiller()
  graceful_killer.add_connection(server)
  graceful_killer.add_connection(db)

  file_manager = FileManager(config['filesystem'])

  matcher = MatcherWrapper(config['matcher'],
                           file_manager)

  print('[*] Image Listener Worker configurado. Esperando mensajes para procesar. Para salir usar CTRL+C')
  server.start_consuming()