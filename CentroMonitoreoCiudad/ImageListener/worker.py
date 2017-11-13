#!/usr/bin/python3

from modules.logger import *
from modules.graceful_killer import *
from modules.pika_wrapper_subscriber import *
from modules.db_wrapper import *
from modules.file_manager import *
from modules.matcher_wrapper import *

def callback(ch, method, properties, body):
  payload = json.loads(body.decode('utf-8'))
  logging.debug('Mensaje recibido: %d caras, con %s, %s',len(payload['faces']),payload['location'],payload['timestamp'])
  
  # matcher.compare()

  # faces_found = faces_to_store(payload['faces'])
  # if len(faces_found) > 0:
  #   store_data(payload,faces_found)

if __name__ == '__main__':
  print('Configurando Worker Image Listener')

  with open('./config.json') as config_file:
    config = json.load(config_file)

  set_logger(config['logger']['logging_level'])
  
  db = DBWrapper(config['db'])

  server = PikaWrapperSubscriber( host=config['network']['host_CMB'],
                                  topic=config['network']['topic_cmc'])
  server.set_receive_callback(callback)

  graceful_killer = GracefulKiller()
  graceful_killer.add_connection(server)
  graceful_killer.add_connection(db)

  matcher = MatcherWrapper(config['matcher'],FileManager(config['filesystem']))

  print('[*] Image Listener Worker configurado. Esperando mensajes para procesar. Para salir usar CTRL+C')
  server.start_consuming()