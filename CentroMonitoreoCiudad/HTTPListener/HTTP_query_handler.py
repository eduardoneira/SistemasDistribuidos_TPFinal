#!/bin/python3

import psycopg2
from modules.logger import *
from modules.rpc_server_rabbitmq import *
from modules.face_recognizer_client import *
from modules.graceful_killer import *
from modules.file_manager import *
from modules.face_cropper import *
import pdb
def handle(body):
  request = json.loads(body.decode('utf-8'))
  response = {}
  response['status'] = 'OK'
  with open('../Database/config.json') as file:
     conf_database = json.load(file)
  connection_str = "dbname={} user={} host={} password={}".format(conf_database['dbname'], conf_database['user'], conf_database['host'], conf_database['password'])
  connection_db = psycopg2.connect(connection_str)
  connection_db.autocommit = True
  cursor = connection_db.cursor()
  if (request['type'] == config['requests']['existance']):
    check_existance(request,response, cursor)
  elif (request['type'] == config['requests']['upload']):
    upload(request,response, cursor)
  elif (request['type'] == config['requests']['trajectory']):
    get_trajectory(request,response, cursor)
  else:
    response['status'] = 'ERROR'
    response['message'] = 'Tipo de mensaje invalido'
  cursor.close()
  connection_db.close()
  return json.dumps(response)

def check_existance(request,response, cursor):
  cropped_images = [];
  images = request['images'];
  for key, image in images.items():
      cropped_images.append(cropper.crop_base_64(image)[0]);
  id = face_recognizer_client.predict(cropped_images)[0]
  if id is not None:
    cursor.execute("SELECT * FROM Person WHERE  Person.Id = %s", (id,))
    rows = self.cursor.fetchall();
    response['name'] =  rows[0][0];
    response['surname'] =  rows[0][1];
    response['dni'] =  rows[0][2];
    response['state'] =  rows[0][3];
  else:
    response['status'] = 'NOT OK'

def upload(request,response, cursor):
  cursor.execute("SELECT dni FROM Person WHERE  Person.dni = %s", (request['dni']))
  rows = self.cursor.fetchall();
  if (len(rows) > 0):
      response['status'] = 'NOT OK'
  else:
      cropped_images = [];
      images = request['images'];
      for key, image in images.items():
          cropped_images.append(cropper.crop_base_64(image)[0]);
      id = face_recognizer_client.update(cropped_images);
      response['id'] = str(id)
      if (request['state'] == config['requests']['missing']):
        state = 'missing'
      else:
        state = 'legal_problems'
      for key, image in images.items():
         file_manager.save_person_base64(image,str(id))
      cursor.execute("INSERT INTO Person (Id, state, name, surname, dni) VALUES (%s,%s, %s, %s,%s)",(id,state,request['name'], request['surname'], request['dni'],))

def get_trajectory(request,response, cursor):
    cursor.execute("SELECT Id FROM Person WHERE  Person.dni = %s", (request['dni']))
    rows = self.cursor.fetchall();
    if (len(rows) == 0):
        response['status'] = 'NOT OK'
    else:
        cursor.execute("SELECT * FROM BigPic WHERE  BigPic.HashBigPic IN (SELECT CropFace.HashBigPic FROM CropFace WHERE CropFace.id = %s)", (id))
        rows = cursor.fetchall()
        if (len(rows) == 0):
            response['status'] = 'NOT OK'
        else:
            points=[]
            for row in rows:
              big_pic_b64 =  file_manager.get_bigpic_base64(row[0])
              point = {"lat": row[1], "lng": row[2], 'image': big_pic_b64, "timestamp": str(row[3])}
              points.append(point)
            response['coordinates'] = points
            response['dni'] =  request['dni']

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

  server = RPCServer( host=config['host_HTTP'],
                      queue=config['queue_http'],
                      request_callback_main=handle)

  face_recognizer_client = FaceRecognizerClient(host=config['host_FaceRecog'],
                                                queue_send=config['queue_send_face_recognizer'],
                                                queue_receive=config['queue_receive_face_recognizer'])

  cropper = FaceCropper()

  graceful_killer = GracefulKiller()
  graceful_killer.add_connection(server)
  graceful_killer.add_connection(face_recognizer_client)
  graceful_killer.add_connection(cursor)
  graceful_killer.add_connection(connection_db)

  print('Comenzando a escuchar mensajes rpc')
  server.start()
