#!/bin/python3

import unittest
import sys

sys.path.insert(0, '../')
from modules.feature_matcher import *

class TestFeatureMatchingInsideImage(unittest.TestCase):

  def setUp(self):
    self.matcher = FeatureMatcher(10)
    
    fd = open('got.jpg','rb')
    self.big_img = fd.read()
    fd.close()

    fd = open('jon_snow1.jpg','rb')
    self.face = fd.read()
    fd.close()
  
  def test_crop_face(self):
    img1 = self.matcher.bytes_to_img(self.big_img)
    img2 = self.matcher.bytes_to_img(self.face)
    self.matcher.compare_and_draw(img1,img2)

if __name__ == '__main__':
  unittest.main()
