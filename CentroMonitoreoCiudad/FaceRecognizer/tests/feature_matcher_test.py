#!/bin/python3

import unittest
import sys

sys.path.insert(0, '../')
from modules.feature_matcher import *
from modules.image_normalizer import *

class TestFeatureMatchingInsideImage(unittest.TestCase):

  def setUp(self):
    self.matcher = FeatureMatcher(feature_extractor='SURF',
                                  upright=True,
                                  min_match_count=4)
    
    with open('edu_photo1.jpg','rb') as fd:
      self.img1 = fd.read()

    with open('edu_photo2.jpg','rb') as fd:
      self.img2 = fd.read()
  
  def test_crop_face(self):
    img1_cv = self.matcher.bytes_to_img(self.img1)
    img2_cv = self.matcher.bytes_to_img(self.img2)
    self.matcher.compare_and_draw(img1_cv,img2_cv)

  # def test_normalization(self):
  #   image = self.matcher.bytes_to_img(self.img1)
  #   image = ImageNormalizer.resize(image,500,500)
    # cv2.imshow('image',image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()



if __name__ == '__main__':
  unittest.main()
