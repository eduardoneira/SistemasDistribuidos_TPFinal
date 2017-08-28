#!/bin/python3

import picamera
from modules.abstract_camera import *

class RaspCamera(AbstractCamera):

  CAPTURE_FILENAME = 'rasp_image.jpg'

  def  __init__(self):
    super().__init__()
    self.camera = picamera.PiCamera()
    #TODO: config camera

  def get_frame(self):
    filepath = self.PATH_IMG() + self.CAPTURE_FILENAME
    self.camera.capture(filepath)

    with open(filepath,'rb') as image:
      img_b64 = self.base64(image)

    os.remove(filepath)      

    return img_b64

  def close(self):
    self.camera.close()
