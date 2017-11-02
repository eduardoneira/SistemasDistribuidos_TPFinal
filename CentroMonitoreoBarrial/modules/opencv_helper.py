#!/bin/python3

import numpy as np
import cv2

def bytes_to_image(image):
  nparr = np.fromstring(image, np.uint8)
  return cv2.imdecode(nparr, 0)                 #Black and white

def image_to_bytes(image):
  r, buff = cv2.imencode('.jpg', image)
  return buff

def show(image):
  cv2.imshow('image',image)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

def save_image(filename,image):
  cv2.imwrite(filename,image)