#!/usr/bin/python3

from cachetools import LRUCache
from modules.image_processing.surf_feature_matcher import *
import pdb

class MatcherWrapper:

  def __init__(self, config, file_manager):
    self.file_manager = file_manager
    self.matcher = SURFFeatureMatcher(min_match_count=config['min_match'])
    self.keypoints = LRUCache(maxsize=config['mem_size'])

  def find_match(self, image, ids):
    processed_image = self.matcher.find_features_base64(image);
    
    best_id = None
    max_good_matches = 0
    
    for id in ids:
      id_keypoints = self._get_keypoints(id)
      
      if (self.matcher.match_descriptors(processed_image[0], processed_image[1], id_keypoints[0], id_keypoints[1])):
        if (len(self.matcher.good_matches) > max_good_matches):
          best_id = id
          max_good_matches = len(self.matcher.good_matches)

    return best_id

  def dump_keypoints(self, id, image):
    keypoints, descriptors = self.matcher.find_features_base64(image)
    self.file_manager.dump_keypoints(keypoints, descriptors, id)

  def _get_keypoints(self, id):
    try:
      return self.keypoints[id]
    except KeyError:
      self.keypoints[id] = self.file_manager.load_keypoints(id)
      return self.keypoints[id]