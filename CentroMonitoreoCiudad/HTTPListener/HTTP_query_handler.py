#!/bin/python3

import json
import psycopg2

from modules.logger import *
from modules.rpc_server_rabbitmq import *
from modules.face_recognizer_client import *
from modules.graceful_killer import *
from modules.file_manager import *

#TODO: save in FS
def handle(request):
  request = json.load(request)
  response = {}
  response['status'] = 'OK'
    
  if (request.type == config['requests']['existance']):
    id = face_recognizer_client.predict([request['image']])[0]
    response['found'] = (id is not None)
  elif (request.type == config['requests']['upload']):
    id = face_recognizer_client.update(request['image'])
    response['id'] = str(id)
    #database.execute('INSERT INTO person (hashperson,state) VALUES (%s,%s)',(str(id),request['state']))
    cursor.execute("""INSERT INTO Person (HashPerson,state) VALUES (%s,%s)""",str(id),request['state'])
    file_manager.save_person_base64(request['image'],str(id))
  elif (request.type == config['requests']['trajectory']):
    id = face_recognizer_client.predict([request['image']])[0]
    if id is not None:
      #database.execute('SELECT DISTINCT B.lat, B.lng FROM cmcdatabase.cropface C, cmcdatabase.bigpic B WHERE C.hashBigPic = B.hashBigPic AND C.HashPerson == (%s)',str(id))
      cursor.execute("SELECT DISTINCT B.lat, B.lng FROM cmcdatabase.cropface C, cmcdatabase.bigpic B WHERE C.hashBigPic = B.hashBigPic AND C.HashPerson == (%s)", id)
      response['coordinates'] = cursor.fetchone()
  else:
    response['status'] = 'ERROR'
    response['message'] = 'Tipo de mensaje invalido'

  return json.dumps(response)

if __name__ == '__main__':
  print('Configurando CMC Query Handler')

  with open('./config.json') as config_file:
    config = json.load(config_file)

  with open('../Database/config.json') as file:
    conf_database = json.load(file)

  file_manager = FileManager(config)
  set_logger(config['logging_level'])

  connection_str = "dbname={} user={} host={} password={}".format(conf_database['dbname'], conf_database['user'], conf_database['host'], conf_database['password'])
  connection_db = psycopg2.connect(connection_str)
  connection_db.autocommit = True

  cursor = connection_db.cursor()

  server = RPCServer( host='localhost',
                      queue=config['queue_http'],
                      request_callback_main=handle)

  face_recognizer_client = FaceRecognizerClient(host='localhost',
                                                queue_send=config['queue_send_face_recognizer'],
                                                queue_receive=config['queue_receive_face_recognizer'])

  graceful_killer = GracefulKiller()
  graceful_killer.add_connection(server)
  graceful_killer.add_connection(face_recognizer_client)
  graceful_killer.add_connection(cursor)
  graceful_killer.add_connection(connection_db)

  print('Comenzando a escuchar mensajes rpc')
  server.start()

