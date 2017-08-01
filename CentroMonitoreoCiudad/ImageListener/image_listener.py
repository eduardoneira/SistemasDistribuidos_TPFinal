#!/bin/python3

import psycopg2
import json
from modules.graceful_killer import *
from modules.logger import *
from modules.pika_wrapper_subscriber import *
from modules.face_recognizer_client import *
from modules.file_manager import *

def store_data(payload, faces_data):
  hash_big_pic = file_manager.save_bigpic_base64(payload['frame'])
  location = payload['location']
  latitude = location[0]
  longitude = location[1]
  timestamp = payload['timestamp']
  cursor.execute("""INSERT INTO BigPic (HashBigPic, Lat, Lng, Timestmp) VALUES (%s, %s, %s, %s)""",(hash_big_pic, latitude, longitude, timestamp))
  
  for face_data in faces_data:
    hash_person = face_data['hash_person']
    hash_crop = face_data['hash_crop']
    cursor.execute("""INSERT INTO CropFace (HashCrop, HashPerson, HashBigPic) VALUES (%s, %s, %s);""",(hash_crop, hash_person, hash_big_pic))

def faces_to_store(faces):
  ids = face_recognizer_client.predict(faces)
  img_to_store = []

  for x in range(0,len(ids)):
    if ids[x] is not None:
      hash_crop = file_manager.save_person_base64(faces[x],ids[x])
      img_to_store.append({ 'hash_person':str(ids[x]),
                            'hash_crop': hash_crop })
  return img_to_store

def callback(ch, method, properties, body):
  payload = json.loads(body)
  logging.debug('Mensaje recibido: {%s,%s}', payload['location'],payload['timestamp'])
  print("Se recibio mensaje de cara. Guardo la imagen grupal y las caras individuales")
  logging.debug('Mensaje recibido: %d caras, con %s, %s',len(payload['faces']),payload['location'],payload['timestamp'])

  faces_found = faces_to_store(payload['faces'])
  if len(faces_found) > 0:
    store_data(payload,faces_found) 


if __name__ == '__main__':
  print('Configurando CMC Image Listener')

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

  server = PikaWrapperSubscriber( host=config['host_CMB'],
                                  topic=config['topic_cmc'])

  server.set_receive_callback(callback)

  face_recognizer_client = FaceRecognizerClient(host='localhost',
                                                queue_send=config['queue_send_face_recognizer'],
                                                queue_receive=config['queue_receive_face_recognizer'])

  graceful_killer = GracefulKiller()
  graceful_killer.add_connection(server)
  graceful_killer.add_connection(face_recognizer_client)
  graceful_killer.add_connection(cursor)
  graceful_killer.add_connection(connection_db)

  print('[*] Esperando mensajes para procesar. Para salir usar CTRL+C')
  server.start_consuming()