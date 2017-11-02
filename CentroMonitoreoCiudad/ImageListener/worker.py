#!/bin/python3

import psycopg2
from modules.graceful_killer import *
from modules.logger import *
from modules.pika_wrapper_subscriber import *
from modules.face_recognizer_client import *
from modules.file_manager import *


def callback(ch, method, properties, body):
  payload = json.loads(body.decode('utf-8'))
  logging.debug('Mensaje recibido: %d caras, con %s, %s',len(payload['faces']),payload['location'],payload['timestamp'])
  
  # matcher.compare()

  # faces_found = faces_to_store(payload['faces'])
  # if len(faces_found) > 0:
  #   store_data(payload,faces_found)

if __name__ == '__main__':
  print('Configurando Worker Feature Matcher')

  file_manager = FileManager(config)

  connection_str = "dbname={} user={} host={} password={}".format(conf_database['dbname'], conf_database['user'], conf_database['host'], conf_database['password'])
  connection_db = psycopg2.connect(connection_str)
  cursor = connection_db.cursor()

  #Abrir conexion con server
  server = PikaWrapperSubscriber( host=config['host_CMB'],
                                  topic=config['topic_cmc'])

  #crear feature matcher propio, fijarse cuantos numeros
  matcher = FeatureMatcher(config['MIN_MATCH'])

  server.set_receive_callback(callback)

  graceful_killer = GracefulKiller()
  graceful_killer.add_connection(server)
  graceful_killer.add_connection(cursor)

  print('[*] Feature Matcher configurado. Esperando mensajes para procesar. Para salir usar CTRL+C')
  server.start_consuming()

