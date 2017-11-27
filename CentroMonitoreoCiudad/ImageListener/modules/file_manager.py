#!/bin/python3

import logging
import os
import base64
import hashlib

class FileManager:

  def __init__(self,config):
    self.config = config
    self.bigpic_path = config['image_database']+config['bigpics']
    self.people_path = config['image_database']+config['people']
    self.keypoints_path = config['image_database']+config['keypoints']

    self.__create_directory(config['image_database'])
    self.__create_directory(self.people_path)
    self.__create_directory(self.bigpic_path)
    self.__create_directory(self.keypoints_path)

  def __create_directory(self,path):
    if not os.path.exists(path):
      logging.debug('Creando directorio en '+path)
      os.makedirs(path)

  def _save_image(self, image, directory):
    self.__create_directory(directory)
    filename = self.SHA1_byte_stream(image)
    filename_fullpath = directory+str(filename)+".jpg"

    with open(filename_fullpath,'wb') as file:
      file.write(image)

    return filename

  def load_keypoints(self,id):
    return load_keypoints(self.keypoints_path+'/'+str(id)+'.kp')

  def save_person_base64(self, image, id):
    return self.save_image(base64.b64decode(image), self.people_path+str(id)+'/')

  def save_bigpic_base64(self, image):
    return self.save_image(base64.b64decode(image), self.bigpic_path)

  def SHA1_byte_stream(self, byte_stream):
    return hashlib.sha1(byte_stream).hexdigest()
