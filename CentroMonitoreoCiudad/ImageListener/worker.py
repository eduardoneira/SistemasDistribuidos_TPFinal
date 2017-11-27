#!/usr/bin/python3

from modules.logger import *
from modules.graceful_killer import *
from modules.pika_wrapper_subscriber import *
from modules.db_wrapper import *
from modules.file_manager import *
from modules.matcher_wrapper import *

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
    cursor.execute("""INSERT INTO CropFace (HashCrop, Id, HashBigPic) VALUES (%s, %s, %s);""",(hash_crop, hash_person, hash_big_pic))


def callback(ch, method, properties, body):
  payload = json.loads(body.decode('utf-8'))
  logging.debug('Mensaje recibido: %d caras, con %s, %s',len(payload['faces']),payload['location'],payload['timestamp'])
  
  for face in payload['faces']:  
    cursor.execute("SELECT id FROM Person")
    ids = self.cursor.fetchall()
    best_id = matcher.find_match(face, ids)

    if best_id
      logging.debug('Se encontro un match con '+id+'. Guardando en sistema')
      #guardar que cara agarrar
    else 
      logging.debug('No se encontro un match. Descartando')

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

  matcher = MatcherWrapper(config['matcher'],
                           FileManager(config['filesystem']))

  print('[*] Image Listener Worker configurado. Esperando mensajes para procesar. Para salir usar CTRL+C')
  server.start_consuming()