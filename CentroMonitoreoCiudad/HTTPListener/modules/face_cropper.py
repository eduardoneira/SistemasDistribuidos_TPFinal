#!/bin/python3

import numpy as np
import cv2
import base64
import logging

class FaceCropper():

  PATH_HAAR = './haarcascade/haarcascade_frontalface_alt.xml'

  def __init__(self):
    self.face_cascade = cv2.CascadeClassifier(self.PATH_HAAR)

  def crop(self,image):
    images=[]
    image_eq = cv2.equalizeHist(image)
   
    #Parametros para imagen un poco clara
    faces = self.face_cascade.detectMultiScale(image_eq,1.1,2,0,(100,100))
    
    for (x,y,w,h) in faces:
      cropped = image[y:y+h,x:x+w]
      logging.debug('face found: [%d,%d,%d,%d]',y,y+h,x,x+w)
      r, buff = cv2.imencode('.jpg', cropped)
      img = base64.b64encode(buff).decode('utf-8')
      images.append(img)

    return images

  #Receives in base64 and returns in base64
  def crop_base_64(self,image):
    return  self.crop(self.bytes_to_image(base64.b64decode(image)))

  def bytes_to_image(self,image):
    nparr = np.fromstring(image, np.uint8)
    return cv2.imdecode(nparr, 0)

  def show(self,image):
    cv2.imshow('image',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

  def save_image(self,filename,image):
    cv2.imwrite(filename,image)