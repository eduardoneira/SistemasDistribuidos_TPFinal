#!/bin/python3

import psycopg2

from modules.logger import *
from modules.rpc_server_rabbitmq import *
from modules.face_recognizer_client import *
from modules.graceful_killer import *
from modules.file_manager import *

def handle(body):
  request = json.loads(body)
  response = {}
  response['status'] = 'OK'

  #TODO: Refactor
  if (request['type'] == config['requests']['existance']):
    id = face_recognizer_client.predict([request['image']])[0]
    if id is not None:
        response['found'] =  get_person_base64(id,cursor)
    else:
        response['found'] = None
  elif (request['type'] == config['requests']['upload']):
    id = face_recognizer_client.update(request['image'])
    response['id'] = str(id)
    if (request['state'] == config['requests']['missing']):
      state = 'missing'
    else:
      state = 'legal_problems'
    filename= file_manager.save_person_base64(request['image'],str(id))
    cursor.execute("INSERT INTO Person (Id,Filepath,state) VALUES (%s, %s,%s)",(id,filename,state))
  elif (request['type'] == config['requests']['trajectory']):
    id = face_recognizer_client.predict([request['image']])[0]
    if id is not None:
      cursor.execute("SELECT * FROM BigPic WHERE  BigPic.HashBigPic IN (SELECT CropFace.HashBigPic FROM CropFace WHERE CropFace.Id = %s)", (id))
      rows = cursor.fetchall()
      points=[]
      for row in rows:
        big_pic_b64 =  file_manager.get_bigpic_base64(row[0])
        point = {"lat": row[1], "lng": row[2], 'image': big_pic_b64, "timestamp": row[3]}
        points.append(point)
      response['coordinates'] = points
      response['bestmatch'] =  file_manager.get_person_base64(id,cursor)
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