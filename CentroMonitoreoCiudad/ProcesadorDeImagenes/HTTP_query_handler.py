#!/bin/python3

import json
import psycopg2

from ProcesadorDeImagenes.modules.logger import *
from ProcesadorDeImagenes.modules.rpc_server_rabbitmq import *
from ProcesadorDeImagenes.modules.LBPH_wrapper import *

with open('./ProcesadorDeImagenes/config.json') as config_file:
  config = json.load(config_file)

def handle(request,database,face_recognizer):
    request = json.load(request)
    response = {}
    response['status'] = 'OK'
    with open('./Database/config.json') as f:
        conf_database = json.load(f)
        connection_str = "dbname={} user={} host={} password={}".format(conf_database['dbname'], conf_database['user'], conf_database['host'], conf_database['password'])
        connection = psycopg2.connect(connection_str)
        cursor = connection.cursor()
        if (request.type == config['requests']['existance']):
            id = face_recognizer.predict_base64(request.image)
            response['found'] = (id is not None)
        elif (request.type == config['requests']['upload']):
            face_recognizer.predict_base64(request.image)
            response['id'] = str(id)
            #database.execute('INSERT INTO person (hashperson,state) VALUES (%s,%s)',(str(id),request['state']))
            cursor.execute("""INSERT INTO Person (HashPerson,state) VALUES (%s,%s)""",id,request['state'])
            connection.commit()
        elif (request.type == config['requests']['trajectory']):
            id = face_recognizer.predict_base64(request.image)
        if id is not None:
            #database.execute('SELECT DISTINCT B.lat, B.lng FROM cmcdatabase.cropface C, cmcdatabase.bigpic B WHERE C.hashBigPic = B.hashBigPic AND C.HashPerson == (%s)',str(id))
            cursor.execute("SELECT DISTINCT B.lat, B.lng FROM cmcdatabase.cropface C, cmcdatabase.bigpic B WHERE C.hashBigPic = B.hashBigPic AND C.HashPerson == (%s)", id)
            response['coordinates'] = cursor.fetchone()
            connection.commit()
        else:
            response['status'] = 'ERROR'
            response['message'] = 'Tipo de mensaje invalido'
        cursor.close()
        connection.close()
    return json.dumps(response)

def HTTP_query_handler_run(face_recognizer):
  print('Configurando CMC Query Handler')

  set_logger(config['logging_level'])

  server = RPCServer( host=config['host_HTTP'],
                      queue=config['queue_http'],
                      request_callback_main=handle,
                      recognizer=face_recognizer)

  print('Comenzando a escuchar mensajes rpc')
  server.start()
def HTTP_query_handler_start():
    HTTP_query_handler_run(ConcurrentLBPHWrapper(config['MIN_MATCH_PROBABILITY'],config['MIN_UPDATE_PROBABILITY']))
