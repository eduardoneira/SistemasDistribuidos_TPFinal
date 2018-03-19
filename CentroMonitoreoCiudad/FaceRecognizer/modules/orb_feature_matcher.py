#!/bin/python3

from modules.feature_matcher import * 

class ORBFeatureMatcher(FeatureMatcher):

    def __init__(self, min_match_count=5):
        super().__init__(min_match_count, flann_index=self.LSH)

        self.feature_finder = cv2.ORB_create()