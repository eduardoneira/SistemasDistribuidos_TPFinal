#!/bin/python3

import numpy as np
import cv2
import base64
import logging

class FaceCropper():

  PATH_HAAR = './haarcascade/haarcascade_frontalface_alt.xml'

  def __init__(self,config):
    self.face_cascade = cv2.CascadeClassifier(self.PATH_HAAR)
    self.scale_factor = config['scale_factor']
    self.min_neighbours = config['min_neighbours']
    self.min_size = (tuple(config['min_size']))

  def crop(self,image):
    images=[]

    image_eq = cv2.equalizeHist(image)
    #Params: image, scale_factor, min_neighbours, flags, min_size
    faces = self.face_cascade.detectMultiScale(image_eq,self.scale_factor,self.min_neighbours,0,self.min_size)
    
    for (x,y,w,h) in faces:
      cropped = cv2.resize(image[y:y+h,x:x+w],self.min_size,cv2.INTER_CUBIC)
      logging.debug('face found: [%d,%d,%d,%d]',y,y+h,x,x+w)
      r, buff = cv2.imencode('.jpg', cropped)
      img = base64.b64encode(buff).decode('utf-8')
      images.append(img)

    return images

  #Receives in base64 and returns in base64
  def crop_base_64(self,image):
    return  self.crop(self.bytes_to_img(base64.b64decode(image)))

  def bytes_to_image(self,image):
    nparr = np.fromstring(image, np.uint8)
    img_np = cv2.imdecode(nparr, 0)
    return img_np

  def show(self,image):
    cv2.imshow('image',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

  def save_image(self,filename,image):
    cv2.imwrite(filename,image)
