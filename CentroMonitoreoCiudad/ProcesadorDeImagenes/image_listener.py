#!/bin/python3

import psycopg2
import json
import sys
from ProcesadorDeImagenes.modules.graceful_killer import *
from ProcesadorDeImagenes.modules.logger import *
from ProcesadorDeImagenes.modules.pika_wrapper_subscriber import *
from ProcesadorDeImagenes.modules.Matcher import Matcher
#from ProcesadorDeImagenes.modules.pika_wrapper_publisher import *
from ProcesadorDeImagenes.modules.LBPH_wrapper import *
sys.path.insert(0, '../')
from CentroMonitoreoBarrial.modules.face_cropper import FaceCropper
from Utils.Hash import compute_sha1_from_file
from Utils.File_Manager import save_data_to_file
import Utils.const as CONST
def store_big_pic(payload, cursor, connect, cropper):
    img = cropper.bytes_to_image(payload['frame'])
    hash_big_pic, file_already_exists, filepath = save_data_to_file(img, CONST.BIGPICIMAGECONTAINERFOLDER)
    if not file_already_exists:
        cursor.execute("SELECT * FROM BigPic WHERE  BigPic.HashBigPic = %s", (self.hash_big_pic,))
        rows = cursor.fetchall()
        if len(rows) == 0:
            location = payload['location']
            latitude = location[0]
            longitude = location[1]
            timestamp = payload['timestamp']
            cursor.execute("""INSERT INTO BigPic (HashBigPic, Lat, Lng, Timestmp) VALUES (%s, %s, %s, %s)""",(hash_big_pic, latitude, longitude, timestamp))
            connect.commit()
        else:
            cursor.execute("UPDATE BigPic SET  BigPic (Lat, Lng, Timestmp) VALUES (%s, %s, %s)", (latitude, longitude, timestamp))
def store_crop_faces(payload, cursor, connect, cropper):
    for crop_face in payload['faces']:
        img = cropper.bytes_to_image(crop_face)
        hash_crop, file_already_exists, filepath = save_data_to_file(img, CONST.CROPIMAGECONTAINERFOLDER)
        if not file_already_exists:
            cursor.execute("SELECT * FROM CropFace WHERE  CropFace.HashCrop = %s", (self.hash_crop,))
            rows = cursor.fetchall()
            if len(rows) == 0:
                matcher = Matcher()
                prediction_filename = matcher.predict(filepath)
                if not prediction_filename == None:
                   hash_person = compute_sha1_from_file(prediction_filename)
                   cursor.execute("""INSERT INTO CropFace (HashCrop, HashPerson, HashBigPic) VALUES (%s, %s, %s, %s);""",(hash_crop,hash_person, hash_big_pic))
                   connect.commit()
def callback(ch, method, properties, body):
    cropper = FaceCropper()
    payload = json.loads(body.decode('utf-8'))
    logging.debug('Mensaje recibido: {%s,%s}', payload['location'],payload['timestamp'])
    print("Se recibio mensaje de frame. Guardo la imagen grupal y las caras individuales")
    logging.debug('Mensaje recibido: %d caras, con %s, %s',len(payload['faces']),payload['location'],payload['timestamp'])
    with open('./Database/config.json') as f:
        conf = json.load(f)
        connection_str = "dbname={} user={} host={} password={}".format(conf['dbname'], conf['user'], conf['host'], conf['password'])
        connection = psycopg2.connect(connection_str)
        cursor = connection.cursor()
        store_big_pic(payload, cursor, connection, cropper)
        store_crop_faces(payload, cursor, connection, cropper)
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
