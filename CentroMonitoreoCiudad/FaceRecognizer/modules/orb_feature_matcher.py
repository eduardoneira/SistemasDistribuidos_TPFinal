#!/bin/python3

from modules.feature_matcher import * 

class ORBFeatureMatcher(FeatureMatcher):

  def __init__(self, min_match_count, _edge_threshold=10, _sigma=1.1):
    super.__init__(min_match_count)

    self.feature_finder = cv2.ORB_create()