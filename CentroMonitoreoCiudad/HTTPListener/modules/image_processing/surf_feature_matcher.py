#!/bin/python3

from modules.image_processing.feature_matcher import * 

class SURFFeatureMatcher(FeatureMatcher):

  def __init__(self, upright=True, min_match_count=5, threshold=400):
    super().__init__(min_match_count)

    self.feature_finder = cv2.xfeatures2d.SURF_create(threshold, extended=True)
    self.feature_finder.setUpright(upright)