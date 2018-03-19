#!/bin/python3

from modules.feature_matcher import * 

class SIFTFeatureMatcher(FeatureMatcher):

    def __init__(self, min_match_count, edge_threshold=10, sigma=1.1):
        super.__init__(min_match_count, flann_index=self.KDTREE)

        self.feature_finder = cv2.xfeatures2d.SIFT_create(edge_threshold=edge_threshold, sigma=sigma)