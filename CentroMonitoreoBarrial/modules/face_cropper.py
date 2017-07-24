#!/bin/python3

import numpy as np
import cv2

class FaceCropper():

  def __init__(self):
    self.face_cascade = cv2.CascadeClassifier('../haarcascade/haarcascade_frontalface_alt.xml')
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
      print('[%d,%d,%d,%d]',y,y+h,x,x+w)
      
      images.append(cropped)
      # cv2.imwrite('img'+str(i)+'.jpg',cropped)
      # cv2.rectangle(img_np,(x,y),(x+w,y+h),(255,0,0),2)


    return images

  def __show(self,image):
    cv2.imshow('image',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

