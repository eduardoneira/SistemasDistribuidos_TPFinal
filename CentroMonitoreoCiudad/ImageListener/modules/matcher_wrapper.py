#!/usr/bin/python3

class MatcherWrapper:

  def __init__(self, config, file_manager):
    self.matcher = FeatureMatcher(config['min_match'])
    self.file_manager = file_manager

  def find_match(self, image, ids):

    return None