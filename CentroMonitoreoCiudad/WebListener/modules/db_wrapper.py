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
  
  def find_person_with_person_image(self, id):
    self.cursor.execute("SELECT * FROM Person WHERE Person.id = (SELECT person_id FROM PersonImage where PersonImage.id = %s);",(str(id),))
    return self.cursor.fetchone()
  
  def find_person(self, id):
    self.cursor.execute("SELECT * FROM Person WHERE Person.id = %s",(str(id),))
    return self.cursor.fetchone()
  
  def find_person_by_dni(self, dni):
    self.cursor.execute("SELECT * FROM Person WHERE Person.dni = %s",(str(dni),))
    return self.cursor.fetchone()

  def save_person(self, dni, state, name, surname):
    self.cursor.execute("INSERT INTO Person (dni, state, name, surname) VALUES (%s,%s,%s,%s);",(dni, state, name, surname))

  def save_person_image(self, id, person_id):
    self.cursor.execute("INSERT INTO PersonImage (id, person_id) VALUES (%s,%s);",(id, person_id))
  
  def find_big_pictures(self, id):
    self.cursor.execute("SELECT * FROM BigPicture WHERE BigPicture.id IN (SELECT Face.bigpic_id FROM Face WHERE Face.person_id = %s)", (id,))
    return self.cursor.fetchall()
    
  def close(self):
    self.cursor.close()
    self.connection_db.close()

  def __map_index(self, array, index):
    result = []

    for row in array:
      result.append(row[index])

    return result