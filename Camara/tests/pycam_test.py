#!/bin/pýthon3


import unittest
import picamera

class TestCamera(unittest.TestCase):

  def test_get_camara(self):
    camera = picamera.PiCamera()

    camera.capture('pycam_image.jpg')

if __name__ == '__main__':
  unittest.main()