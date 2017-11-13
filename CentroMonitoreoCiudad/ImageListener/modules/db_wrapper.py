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

  def get_people_uploaded(self):
    #return list of ids
    return []
  
  def save_match(self,id,big_pic_path,face_path):

  def close(self):
    self.cursor.close()
    self.connection_db.close()
  