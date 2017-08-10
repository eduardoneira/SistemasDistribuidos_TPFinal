#!/bin/python3

import logging
import os
import base64
import hashlib

class FileManager:

  def __init__(self,config):
    self.person_path = config['image_database']+config['person']
    self.bigpic = config['image_database']+config['bigpic']

    self.__create_directory(config['image_database'])
    self.__create_directory(self.person_path)
    self.__create_directory(self.bigpic)

  def __create_directory(self,path):
    if not os.path.exists(path):
      logging.debug('Creando directorio en '+path)
      os.makedirs(path)


  def save_image(self,image,directory):
    self.__create_directory(directory)
    filename = self.SHA1_byte_stream(image)
    filename_fullpath = directory+str(filename)+".jpg"

    with open(filename_fullpath,'wb') as file:
      file.write(image)

    return filename

  def save_person_base64(self,image,id):
    return self.save_image(base64.b64decode(image),self.person_path+str(id)+'/')

  def save_bigpic_base64(self,image):
    return self.save_image(base64.b64decode(image),self.bigpic)

  def SHA1_byte_stream(self,byte_stream):
    sha1 = hashlib.sha1(byte_stream)
    return sha1.hexdigest()
