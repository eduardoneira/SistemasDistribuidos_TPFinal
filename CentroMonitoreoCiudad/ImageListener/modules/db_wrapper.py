#!/usr/bin/python3

import psycopg2

class DBWrapper:

  def __init__(self,config):
    connection_str = "dbname={} user={} host={} password={}".format(config['dbname'], 
                                                                    config['user'], 
                                                                    config['host'], 
                                                                    config['password'])
    self.connection_db = psycopg2.connect(connection_str)
    self.cursor = self.connection_db.cursor()

  def most_wanted_people(self):
    self.cursor.execute("SELECT id FROM Person;")
    return self.cursor.fetchall()
  
  def save_match_person(self, id, big_pic_id):
      cursor.execute("""INSERT INTO Faces (id, big_pictures_id) VALUES (%s, %s, %s);""",(id, big_pic_id))

  def save_match_big_pic(self, id, latitude, longitude, timestamp):
    self.cursor.execute("""INSERT INTO BigPictures (id, latitude, longitude, timestamp) VALUES (%s, %s, %s, %s)""",(id, latitude, longitude, timestamp))

  def close(self):
    self.cursor.close()
    self.connection_db.close()
  