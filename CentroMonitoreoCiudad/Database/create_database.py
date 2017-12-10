#!/usr/bin/python3

import json
import psycopg2

if __name__ == '__main__':
  with open('./config.json') as config_file:
    config = json.load(config_file)

  connection_str = "dbname={} user={} host={} password={}".format(config['dbname'], 
                                                                  config['user'], 
                                                                  config['host'], 
                                                                  config['password'])
  connection_db = psycopg2.connect(connection_str)

  cursor = connection_db.cursor()

  cursor.execute("""CREATE TABLE Person (id char(40) SERIAL PRIMARY KEY, char(9) integer NOT NULL, state char(20) NOT NULL, name char(20) NOT NULL, surname char(20) NOT NULL);""")
  cursor.execute("""CREATE TABLE PersonImage (id char(40) PRIMARY KEY, person_id char(40) REFERENCES Person);""")
  cursor.execute("""CREATE TABLE BigPicture (id char(40) PRIMARY KEY, latitude double precision NOT NULL, longitude double precision NOT NULL, time_stamp timestamp);""")
  cursor.execute("""CREATE TABLE Face (id char(40) PRIMARY KEY, person_id char(40) REFERENCES Person, bigpic_id char(40) REFERENCES BigPicture);""")

  connection_db.commit()

  cursor.close()
  connection_db.close()