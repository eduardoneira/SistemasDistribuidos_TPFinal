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
    with open(directory+filename,'wb') as file:
      file.write(image)

  def save_person_base64(self,image,id):
    self.save_person(base64.b64decode(image),id)

  def __SHA1_byte_stream(self,byte_stream):
    return hashlib.sha1(byte_stream).hexdigest()