#!/bin/python3

import numpy as np
import cv2
import base64
import logging

class FaceCropper():

  def __init__(self):
    self.face_cascade = cv2.CascadeClassifier('./haarcascade/haarcascade_frontalface_alt.xml')
    # self.body_cascade = cv2.CascadeClassifier('../haarcascade/haarcascade_fullbody.xml')

  
  def crop(self,image):
    images=[]
    
    nparr = np.fromstring(image, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

    #Parametros para imagen un poco clara
    faces = self.face_cascade.detectMultiScale(gray,1.1,2,0,(20,20))
    for (x,y,w,h) in faces:
      cropped = img_np[y:y+h,x:x+w]
      logging.debug('face found: [%d,%d,%d,%d]',y,y+h,x,x+w)
      
      images.append(cv2.imencode('.jpg', cropped)[1].tostring())

    return images

  #Receives in base64 and returns in base64
  def crop_base_64(self,image):
    images = self.crop(base64.b64decode(image))
    for img in images:
      img = base64.b64encode(img).decode('utf-8')

    return images

  def bytes_to_image(self,image):
    nparr = np.fromstring(image, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img_np

  def show(self,image):
    cv2.imshow('image',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

  def save_image(self,filename,image):
    cv2.imwrite(filename,image)