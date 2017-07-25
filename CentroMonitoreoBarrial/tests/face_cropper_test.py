#!/bin/python3

import unittest
import sys

sys.path.insert(0, '../')
from modules.face_cropper import *

class TestFaceCropper(unittest.TestCase):

  def setUp(self):
    fd = open('got.jpg','rb')
    self.test_image = fd.read()
    fd.close()

  def test_crop_face(self):
    cropper = FaceCropper()
    cropped_images = cropper.crop(self.test_image)
    self.assertEqual(len(cropped_images),5)
    
    # with open("face.jpg",'wb') as f:
    #   f.write(cropped_images[0])

if __name__ == '__main__':
  unittest.main()