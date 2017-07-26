#!/bin/python3

import numpy as np
import cv2

class LBPHWrapper:

  FILENAME = 'LBPH_dump'

  def __init__(self,min_match_probability,min_update_probability):
    self.recognizer = cv2.face.LBPHFaceRecognizer_create()
    self.images_processed = 0
    self.MIN_MATCH_PROBABILITY = min_match_probability
    self.MIN_UPDATE_PROBABILITY = min_update_probability

  def update(self,img,id):
    # img_array = np.array(img,'uint8')
    self.recognizer.update([img],np.array([id]))

  def predict(self,img):
    nrb_predicted, conf = self.recognizer.predict(img)
    
    print("La imagen que es mas cercana es "+str(nrb_predicted)+" con confianza "+str(conf))
    if (conf>=self.MIN_MATCH_PROBABILITY):
      if (conf >= self.MIN_UPDATE_PROBABILITY):
        self.update(img,nrb_predicted)  
      return str(nrb_predicted)

    return "NOT FOUND"

  def train(self,images,labels):
    self.recognizer.train(images,np.array(labels))

  def save():
    self.recognizer.save(self.FILENAME)

  def load():
    self.recognizer.load(self.FILENAME)    

  def predict_base64(self,image_base64):
    image = self.base64_to_img(image_base64)

    return self.predict(image)

  def update_base64(self,image_base64,id):
    image = self.base64_to_img(image_base64)

    return self.update(image,id) 

  def bytes_to_img(self,image_bytes):
    nparr = np.fromstring(image_bytes, np.uint8)
    img_np = cv2.imdecode(nparr, 0)
    return img_np

  def base64_to_img(self,image_base64):
    return self.bytes_to_img(base64.b64decode(image_base64))
 