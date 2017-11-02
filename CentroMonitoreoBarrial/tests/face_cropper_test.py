#!/bin/python3

import unittest
import sys

sys.path.insert(0, '../')
from modules.face_cropper import *

class TestFaceCropper(unittest.TestCase):

  def setUp(self):
    self.config = {
                    'scale_factor' : 1.1,
                    'min_neighbours' : 2,
                    'min_size' : [200,
                                  200]
                  }
    with open('wachos.jpg','rb') as fd:
      self.test_image = fd.read()

  def test_crop_face(self):
    cropper = FaceCropper(self.config)
    img_cv = cropper.bytes_to_image(self.test_image)
    cropped_images = cropper.crop(img_cv)

    for index, cropped in enumerate(cropped_images):
      with open(str(index)+'.jpg','wb') as file:
        file.write(cropped)

    # self.assertEqual(len(cropped_images),5)
    
    # with open("face.jpg",'wb') as f:
    #   f.write(cropped_images[0])

if __name__ == '__main__':
  unittest.main()