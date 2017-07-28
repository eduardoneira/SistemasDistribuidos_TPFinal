import psycopg2
def callback(ch, method, properties, body):
    with open('../config.json') as f:
        conf = json.load(f)
        connection_str = "dbname={} user={} host={} password={}".format(conf['dbname'], conf['user'], conf['host'], conf['password'])
        connection = psycopg2.connect(connection_str)
        cursor = connection.cursor()
        payload = json.loads(body)
        logging.debug('Mensaje recibido: %d caras, con %s, %s',len(payload['faces']),payload['location'],payload['timestamp'])
        #hash_big_pic = Hash.compute(payload['frame'])
        #location = payload['location']
        #latitude = location[0]
        #longitude = location[1]
        #timestamp = location['timestamp']
        #cursor.execute("""INSERT INTO BigPic (HashBigPic, Lat, Lng, Timestamp) VALUES (%s, %s, %s, %s);""",(hash_big_pic, latitude, longitude, timestamp))
        for crop_face in payload['faces']:
          # if feature_matcher.compare_to_all_faces(crop_face) == MATCH:
          #     img = feature_matcher.getMatch()
          #     hash_person = Hash.compute(img)
          #     hash_crop = Hash.compute(crop_face)
          #     cursor.execute("""INSERT INTO CropFace (HashCrop, HashPerson, HashBigPic) VALUES (%s, %s, %s, %s);""",(hash_crop,hash_person, hash_big_pic))
def main():
    server = PikaWrapperSubscriber( host='localhost',
                                    topic=config['topic_cmc'],
                                    queue=config['queue'])
    killer = GracefulKiller()
    killer.add_connection(server)

    server.set_receive_callback(callback)

    print('[*] Esperando mensajes para procesar. Para salir usar CTRL+C')
    server.start_consuming()
    # crear predictor
if __name__ == '__main__':
    main()
