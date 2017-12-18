#!/usr/bin/python3

import psycopg2

class DBWrapper:

  def __init__(self,config):
    connection_str = "dbname={} user={} host={} password={}".format(config['dbname'], 
                                                                    config['user'], 
                                                                    config['host'], 
                                                                    config['password'])
    self.connection_db = psycopg2.connect(connection_str)
    self.connection_db.autocommit = True
    self.cursor = self.connection_db.cursor()

  def person_images(self):
    self.cursor.execute("SELECT id FROM PersonImage;")
    return self.__map_index(self.cursor.fetchall(),0)

  def person_id_by_person_image_id(self, id):
    self.cursor.execute("SELECT person_id FROM PersonImage WHERE PersonImage.id = %s;",(id,))
    return self.cursor.fetchone()[0]
  
  def save_match_person(self, id, person_id, big_pic_id):
    self.cursor.execute("""INSERT INTO Face (id, person_id, bigpic_id) VALUES (%s, %s, %s);""",(id, person_id, big_pic_id))

  def save_match_big_pic(self, id, latitude, longitude, timestamp):
    self.cursor.execute("""INSERT INTO BigPicture (id, latitude, longitude, time_stamp) VALUES (%s, %s, %s, %s);""",(id, latitude, longitude, timestamp))

  def close(self):
    self.cursor.close()
    self.connection_db.close()
  
  def __map_index(self, array, index):
    result = []

    for row in array:
      result.append(row[index])

    return result