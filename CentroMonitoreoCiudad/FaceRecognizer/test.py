#!/usr/bin/python3

import base64
import pdb
from modules.surf_feature_matcher import *
from modules.face_cropper import *

def config_cropper():
  return {
           "scale_factor" : 1.1,
           "min_neighbours" : 2,
           "min_size" : [180 ,180],
           "default_size" : [200,200],
           "shrink_factor": 0.20
         }

if __name__ == '__main__':

  feature_matcher = SURFFeatureMatcher(min_match_count=4, threshold=800)
  cropper = FaceCropper(config_cropper())
  
  with open('tests/-1.jpg','rb') as fd:
    img1 = fd.read()

  with open('tests/5.jpg','rb') as fd:
    img2 = fd.read()
  
  img1_b64 = base64.b64encode(img1).decode('utf-8')
  img2_b64 = base64.b64encode(img2).decode('utf-8')

  img1_cropped = cropper.crop_base64(img1_b64)[0]
  img2_cropped = cropper.crop_base64(img2_b64)[0]

  img1_features = feature_matcher.find_features_base64(img1_cropped)  
  img2_features = feature_matcher.find_features_base64(img2_cropped)

  # print(feature_matcher.match_descriptors(img1_features[1],img2_features[1]))  
  feature_matcher.compare_and_draw_base64(img1_cropped, img2_cropped)