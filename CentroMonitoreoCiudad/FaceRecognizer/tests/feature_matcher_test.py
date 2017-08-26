#!/bin/python3

import unittest
import sys

sys.path.insert(0, '../')
from modules.feature_matcher import *
from modules.image_normalizer import *

class TestFeatureMatchingInsideImage(unittest.TestCase):

  def setUp(self):
    self.matcher = FeatureMatcher(10,400)
    
    fd = open('img2.jpg','rb')
    self.img1 = fd.read()
    fd.close()

    fd = open('img1.jpg','rb')
    self.img2 = fd.read()
    fd.close()
  
  def test_crop_face(self):
    img1_cv = self.matcher.bytes_to_img(self.img1)
    img2_cv = self.matcher.bytes_to_img(self.img2)
    # self.matcher.compare_and_draw(img1_cv,img2_cv)

  def test_normalization(self):
    image = self.matcher.bytes_to_img(self.img1)
    image = ImageNormalizer.resize(image,500,500)
    cv2.imshow('image',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
  unittest.main()
