#!/bin/python3

import logging
import glob
import os
import hashlib
import base64

image_path = './img_processed/'

def set_logger(logging_level):
  if not os.path.exists('./log/'):
    os.makedirs('./log/')

  #Para no sobreescribir
  id = len(glob.glob("./log/*.log")) +1

  logging.basicConfig(  level=logging_level,
                        format='%(asctime)s %(levelname)-8s CMB      '+ str(os.getpid()) +'    %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='./log/CMB'+str(id)+'.log',
                        filemode='w')

  logging.getLogger('pika').setLevel(logging.WARNING)

def set_image_directory():
  if not os.path.exists(image_path):
    os.makedirs(image_path)

def _save_image(img):
  filename = str(hashlib.sha1(img).hexdigest())
  with open(image_path+filename+".jpg",'wb') as file:
    file.write(img)

def save_image_b64(big_pic, faces): 
    _save_image(base64.b64decode(big_pic))
    for face in faces:
      _save_image(base64.b64decode(face))
