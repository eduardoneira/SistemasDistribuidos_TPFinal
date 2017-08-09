#!/bin/python3

import logging
import os
import base64
import hashlib

class FileManager:

  def __init__(self,config):
    self.person_path = config['image_database']+config['person']
    self.bigpic_path = config['image_database']+config['bigpic']

    self.__create_directory(config['image_database'])
    self.__create_directory(self.person_path)
    self.__create_directory(self.bigpic_path)

  def __create_directory(self,path):
    if not os.path.exists(path):
      logging.debug('Creando directorio en '+path)
      os.makedirs(path)


  def save_person(self,image,id):
    directory = self.person_path+str(id)+'/'
    self.__create_directory(directory)
    filename = str(self.__SHA1_byte_stream(image))
    with open(directory+filename+".jpg",'wb') as file:
      file.write(image)
    return filename

  def save_person_base64(self,image,id):
    return self.save_person(base64.b64decode(image),id)

  def __SHA1_byte_stream(self,byte_stream):
    return hashlib.sha1(byte_stream).hexdigest()

  def get_image_base64(self,filename,directory):
    with open(directory+filename+".jpg", 'rb') as file:
      bestmatch_b64 =  base64.b64encode(file.read()).decode('utf-8')

    return bestmatch_b64
  def get_file_name(self, id, cursor):
      cursor.execute("SELECT Person.Filepath FROM Person WHERE  Person.Id  = %s", (id,))
      row = cursor.fetchone()
      return row[0]
  def get_person_base64(self, id, cursor):
    filename = self.get_file_name(id, cursor)
    return self.get_image_base64(filename,self.person_path+str(id)+'/')

  def get_bigpic_base64(self,filename):
    return self.get_image_base64(filename,self.bigpic_path+'/')
