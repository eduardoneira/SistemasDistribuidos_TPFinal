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

  def most_wanted_people_images(self):
    self.cursor.execute("SELECT id FROM PersonImage;")
    return self.cursor.fetchall()
  
  def save_match_person(self, id, person_id, big_pic_id):
    self.cursor.execute("""INSERT INTO Faces (id, person_id, bigpic_id) VALUES (%s, %s, %s);""",(id, person_id, big_pic_id))

  def save_match_big_pic(self, id, latitude, longitude, timestamp):
    self.cursor.execute("""INSERT INTO BigPictures (id, latitude, longitude, time_stamp) VALUES (%s, %s, %s, %s);""",(id, latitude, longitude, timestamp))

  def close(self):
    self.cursor.close()
    self.connection_db.close()
  