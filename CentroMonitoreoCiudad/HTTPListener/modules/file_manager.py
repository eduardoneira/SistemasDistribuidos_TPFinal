#!/bin/python3

import logging
import os
import base64
import hashlib

class FileManager:

  def __init__(self,config):
    self.person_path = config['image_database']+config['person']

    self.__create_directory(config['image_database'])
    self.__create_directory(self.person_path)

  def __create_directory(self,path):
    if not os.path.exists(path):
      logging.debug('Creando directorio en '+path)
      os.makedirs(path)


  def save_person(self,image,id):
    directory = self.person_path+str(id)+'/'
    self.__create_directory(directory)
    filename = str(self.__SHA1_byte_stream(image))+".jpg"
    with open(filename,'wb') as file:
      file.write(image)

  def save_person_base64(self,image,id):
    self.save_person(base64.b64decode(image),id)

  def __SHA1_byte_stream(byte_stream):
    sha1 = hashlib.sha1()
    sha1.update(byte_stream.encode('utf-8'))
    return sha1.hexdigest()