#!/bin/python3

import numpy as np
import cv2
import pdb
import base64
from tkinter import *
from matplotlib import pyplot as plt 
from modules.opencv_helper import *

class FeatureMatcher:

  __PORC_DISTANCE = 0.7
  __USE_RANSAC = True

  def __init__(self, min_match_count=4):
    self.MIN_MATCH_COUNT = min_match_count

    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 200)
    self.flann = cv2.FlannBasedMatcher(index_params, search_params)

  def _compare_descriptors(self, features_img1, features_img2):
    return self.flann.knnMatch(features_img1, features_img2, k=2)

  def match_image_base64(self, img1, img2):  
    self.features_img1 = self.find_features(base64_to_image(img1)) 
    self.features_img2 = self.find_features(base64_to_image(img2))

    return self.match_descriptors(self.feature_img1[0], self.features_img1[1], self.feature_img2[0], self.features_img2[1])

  def match_descriptors(self, kp1, desc1, kp2, desc2):
    self.good_matches = []

    for m,n in self._compare_descriptors(desc1, desc2):
      if m.distance < self.__PORC_DISTANCE*n.distance:
        self.good_matches.append(m)

    if (len(self.good_matches) > self.MIN_MATCH_COUNT):
      if (self.__USE_RANSAC):
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in self.good_matches ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in self.good_matches ]).reshape(-1,1,2)
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 3.0)
        return (mask.ravel().tolist().count(1) > self.MIN_MATCH_COUNT)
      else:
        return True
    else: 
      return False

  def find_features(self,img):
    img_eq = cv2.equalizeHist(img)
    return self.feature_finder.detectAndCompute(img_eq,None)

  def find_features_base64(self,img):
    return self.find_features(base64_to_image(img))

  def compare_and_draw_base64(self, img1, img2):
    self._compare_and_draw(base64_to_image(img1),base64_to_image(img2))

  def _compare_and_draw(self, img1, img2):
    hash1 = self.find_features(img1)
    hash2 = self.find_features(img2)
    matches = self.flann.knnMatch(hash1[1], hash2[1], k=2)

    good = []
    for m,n in matches:
      if m.distance < self.__PORC_DISTANCE*n.distance:
          good.append(m)
    print("Good matches: "+ str(len(good)))

    if len(good)>self.MIN_MATCH_COUNT:
      src_pts = np.float32([ hash1[0][m.queryIdx].pt for m in good ]).reshape(-1,1,2)
      dst_pts = np.float32([ hash2[0][m.trainIdx].pt for m in good ]).reshape(-1,1,2)
      M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 3.0)
      matchesMask = mask.ravel().tolist()
      print("Mask matches: "+str(matchesMask.count(1)))
      if (matchesMask.count(1) > 0):
        h, w = img1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)
        img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)
    else:
      print( "Not enough matches are found - {}/{}".format(len(good), self.MIN_MATCH_COUNT) )
      matchesMask = None

    draw_params = dict(matchColor = (0,255,0),
                       singlePointColor = (255,0,0),
                       matchesMask = matchesMask,
                       flags = 2)

    img3 = cv2.drawMatches(img1,hash1[0],img2,hash2[0],good,None,**draw_params)
    plt.imshow(img3, 'gray'),plt.show()