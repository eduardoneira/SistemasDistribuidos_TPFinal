#!/bin/python3

import json
import psycopg2

from modules.logger import *
from modules.rpc_server_rabbitmq import *
from modules.LBPH_wrapper import *

with open('config.json') as config_file:    
  config = json.load(config_file)

def handle(request,database,face_recognizer):
  request = json.load(request)
  response = {}
  response['status'] = 'OK'

  if (request.type == config['requests']['existance']):
    id = face_recognizer.predict_base64(request.image)
    respone['found'] = (id is not None)
  elif (request.type == config['requests']['upload']):
    face_recognizer.predict_base64(request.image)    
    response['id'] = str(id)
    #TODO: map to db
  elif (request.type == config['requests']['trajectory']):
    id = face_recognizer.predict_base64(request.image)
    if id is not None:
      database.execute('SELECT DISTINCT latitude, longitude FROM cmcdatabase.CropFace WHERE HashPerson == '+str(id))
      #TODO: join with HashBigPic
      response['coordinates'] = database.fetchone()
  else:
    response['status'] = 'ERROR'
    response['message'] = 'Tipo de mensaje invalido'

  return json.dumps(response)

def HTTP_query_handler_run(face_recognizer):
  print('Configurando CMC Query Handler')

  database_connection = psycopg2.connect("dbname='cmcdatabase' user='postgres' host='localhost' password='postgres'")

  set_logger(config['logging_level'])

  server = RPCServer( host=config['host_HTTP'],
                      queue=config['queue_http'],
                      request_callback_main=handle,
                      database=database_connection.cursor(),
                      recognizer=face_recognizer)

  print('Comenzando a escuchar mensajes rpc')
  server.start()


HTTP_query_handler_run(ConcurrentLBPHWrapper(config['MIN_MATCH_PROBABILITY'],config['MIN_UPDATE_PROBABILITY']))