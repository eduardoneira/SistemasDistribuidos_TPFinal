#!/bin/python3

import numpy as np
import cv2
import base64
import _pickle as pickle

def bytes_to_image(image):
  nparr = np.fromstring(image, np.uint8)
  return cv2.imdecode(nparr, 0)                 #Black and white

def image_to_bytes(image):
  r, buff = cv2.imencode('.jpg', image)
  return buff

def base64_to_image(image):
  return bytes_to_image(base64.b64decode(image))

def show_base64(image):
  show(base64_to_image(image))

def show(image):
  cv2.imshow('image',image)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

def save_image(filename,image):
  cv2.imwrite(filename,image)

def dump_keypoints(keypoints, descriptors, filepath):
  i = 0
  serialization = []
  
  for point in keypoints:
    point_serialization = (point.pt, point.size, point.angle, point.response, point.octave, point.class_id, descriptors[i])
    serialization.append(point_serialization)
    ++i

  with open(filepath,"wb") as file:
    pickle.dump(serialization, file)

def load_keypoints(filepath):
  with open(filepath,"wb") as file:
    serialization = pickle.load(file)
  
  keypoints = []
  descriptors = []
  
  for point in serialization:
    feature = cv2.KeyPoint(x=point[0][0],y=point[0][1],_size=point[1], _angle=point[2], _response=point[3], _octave=point[4], _class_id=point[5])
    descriptor = point[6]
    keypoints.append(feature)
    descriptors.append(descriptor)
  
  return keypoints, np.array(descriptors)