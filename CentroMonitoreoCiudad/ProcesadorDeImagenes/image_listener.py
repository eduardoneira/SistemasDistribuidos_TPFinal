#!/bin/python3


import json
import sys
from ProcesadorDeImagenes.modules.graceful_killer import *
from ProcesadorDeImagenes.modules.logger import *
from ProcesadorDeImagenes.modules.pika_wrapper_subscriber import *
#from ProcesadorDeImagenes.modules.pika_wrapper_publisher import *
from ProcesadorDeImagenes.modules.LBPH_wrapper import *
sys.path.insert(0, '../')
from Utils.Hash import Sha1
def callback(ch, method, properties, body):
    payload = json.loads(body)
    logging.debug('Mensaje recibido: {%s,%s}', payload['location'],payload['timestamp'])
    print("Se recibio mensaje de frame. Comienza el cropeo")
    with open('./Database/config.json') as f:
        conf = json.load(f)
        connection_str = "dbname={} user={} host={} password={}".format(conf['dbname'], conf['user'], conf['host'], conf['password'])
        connection = psycopg2.connect(connection_str)
        cursor = connection.cursor()
        payload = json.loads(body)
        logging.debug('Mensaje recibido: %d caras, con %s, %s',len(payload['faces']),payload['location'],payload['timestamp'])
        #sha1= Sha1()
        #hash_big_pic = sha1.compute(payload['frame'])
        #location = payload['location']
        #latitude = location[0]
        #longitude = location[1]
        #timestamp = location['timestamp']
        #cursor.execute("""INSERT INTO BigPic (HashBigPic, Lat, Lng, Timestmp) VALUES (%s, %s, %s, %s)""",(hash_big_pic, latitude, longitude, timestamp))
        #cursor.commit()
        #for crop_face in payload['faces']:
        #   if feature_matcher.compare_to_all_faces(crop_face) == ONEMATCH:
        #   img = feature_matcher.getMatch()
        #   hash_person = sha1.compute(img)
        #   hash_crop = sha1.compute(crop_face)
        #   cursor.execute("""INSERT INTO CropFace (HashCrop, HashPerson, HashBigPic) VALUES (%s, %s, %s, %s);""",(hash_crop,hash_person, hash_big_pic))
        #   cursor.commit()
        cursor.close()
        connection.close()

# https://stackoverflow.com/questions/3671666/sharing-a-complex-object-between-python-processes
#if __name__ == '__main__':
def image_listener_start():
  print('Configurando CMB')

  with open('./ProcesadorDeImagenes/config.json') as config_file:
    config = json.load(config_file)

  set_logger(config['logging_level'])

  server = PikaWrapperSubscriber( host=config['host_CMB'],
                                  topic=config['topic_cmc'])

  # client = PikaWrapperPublisher(host=config['host_HTTP'],
  #                               topic=config['topic_'])

  #Train or load if there is something from before
  predictor = LBPHWrapper(config['MIN_MATCH_PROBABILITY'],
                          config['MIN_UPDATE_PROBABILITY']
                         )

  killer = GracefulKiller()
  killer.add_connection(server)
  killer.add_predictor(predictor)

  server.set_receive_callback(callback)

  print('[*] Esperando mensajes para procesar. Para salir usar CTRL+C')
  server.start_consuming()
