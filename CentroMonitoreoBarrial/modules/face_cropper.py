#!/bin/python3

import numpy as np
import cv2
import base64
import logging
from modules.opencv_helper import *

class FaceCropper():

  PATH_HAAR = './haarcascade/haarcascade_frontalface_alt.xml'

  def __init__(self,config):
    self.face_cascade = cv2.CascadeClassifier(self.PATH_HAAR)
    self.scale_factor = config['scale_factor']
    self.min_neighbours = config['min_neighbours']
    self.min_size = (tuple(config['min_size']))

  def _crop(self,image):
    images=[]

    image_eq = cv2.equalizeHist(image)
    # TODO: Adjust params to find head
    # Params: image, scale_factor, min_neighbours, flags, min_size
    faces = self.face_cascade.detectMultiScale(image_eq,self.scale_factor,self.min_neighbours,0,self.min_size)
    
    for (x,y,w,h) in faces:
      # TODO: Crop smaller to square face 
      cropped = cv2.resize(image[y:y+h,x:x+w],self.min_size,cv2.INTER_CUBIC)
      logging.debug('Face found: [%d,%d,%d,%d]',y,y+h,x,x+w)
      images.append(image_to_bytes(cropped))

    return images

  def crop(self,image):
    return self._crop(bytes_to_image(image))

  #Receives in base64 and returns in base64
  def crop_base64(self,image):
    cv_image = bytes_to_image(base64.b64decode(image))
    return list(map(lambda img: base64.b64encode(img).decode('utf-8'), self._crop(cv_image)))