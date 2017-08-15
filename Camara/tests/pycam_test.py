#!/bin/pýthon3


import unittest
import picamera

sys.path.insert(0, '../')
from modules.real_camara import *

class TestCamera(unittest.TestCase):

  def test_get_camara(self):
    camera = picamera.PiCamera()

    camera.capture('image.jpg')

if __name__ == '__main__':
  unittest.main()