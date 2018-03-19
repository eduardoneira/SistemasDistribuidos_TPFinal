#!/usr/bin/python3

import pdb
import base64
from modules.surf_feature_matcher import *
from modules.orb_feature_matcher import *
from modules.face_cropper import *

def config_cropper():
  return {
           "scale_factor" : 1.1,
           "min_neighbours" : 2,
           "min_size" : [180 ,180],
           "default_size" : [200,200],
           "shrink_factor": 0.20
         }

# class CompareImageTest(unittest.TestCase):

#   def __crop_image(self, filename, index):
#     with open(filename,'rb') as fd:
#       img = fd.read()
  
#     img_b64 = base64.b64encode(img).decode('utf-8')

#     img_cropped = cropper.crop_base64(img_b64)[index]

#     img_features = feature_matcher.find_features_base64(img_cropped)  

#     return (filename, img_features)

#   def setUp(self):
#     self.cropper = FaceCropper(config_cropper())
  
#     with open("fixtures.json") as file:
#       self.fixtures = json.load(file)

#     self.users = []
#     for user, images in self.fixtures:
#       self.users.append(user)
#       self.images[user] = []
#       for image in images:
#         self.images[user].append(self.__crop_image(image["filename"], image["index"]))

#   def __one_vs_all(self, user_to_test):
#     for image_to_test in self.images[user_to_test]:
#       for user in self.users:
#         total_images = 0

#         for image in self.images[user]:
#           if image_to_test != image 
#             is_match = self.feature_matcher.match_descriptors(image_to_test[1][0], image_to_test[1][1], image[1][0], image[1][1]) 
#             matches_count = self.feature_matcher.good_matches_count
#             print("La imagen ")
  
#   def ORBTest(self):    
#     self.feature_matcher = ORBFeatureMatcher(min_match_count=5)

#     for user in self.users:
#       self.__one_vs_all(user)
    
if __name__ == '__main__':

  feature_matcher = SURFFeatureMatcher(min_match_count=4, threshold=400)
  # feature_matcher = ORBFeatureMatcher(min_match_count=5)
  cropper = FaceCropper(config_cropper())
  
  with open('tests/20.jpg','rb') as fd:
    img1 = fd.read()

  with open('fix/5.jpg','rb') as fd:
    img2 = fd.read()
  
  img1_b64 = base64.b64encode(img1).decode('utf-8')
  img2_b64 = base64.b64encode(img2).decode('utf-8')

  img1_cropped = cropper.crop_base64(img1_b64)[0]
  img2_cropped = cropper.crop_base64(img2_b64)[0]

  img1_features = feature_matcher.find_features_base64(img1_cropped)  
  img2_features = feature_matcher.find_features_base64(img2_cropped)
  # pdb.set_trace()
  print(feature_matcher.match_descriptors(img1_features[0], img1_features[1], img2_features[0], img2_features[1]))  
  print(feature_matcher.good_matches_count)
  feature_matcher.compare_and_draw_base64(img1_cropped, img2_cropped)