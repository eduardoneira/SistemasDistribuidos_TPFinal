#!/bin/python3

import numpy as np
import cv2
import base64
from tkinter import *
from matplotlib import pyplot as plt 

class FeatureMatcher:

  __PORC_DISTANCE = 0.7

  def __init__(self,feature_extractor='SURF',upright=True,min_match_count=10,threshold=500):
    self.MIN_MATCH_COUNT = min_match_count
    self.feature_finder = self.__create_feature_extractor(feature_extractor,upright,threshold)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 100)
    self.flann = cv2.FlannBasedMatcher(index_params, search_params)

  def __create_feature_extractor(self,feature_extractor,upright,threshold):
    if feature_extractor == 'SURF':
      self.feature_finder = cv2.xfeatures2d.SURF_create(threshold=threshold,extended=True)
      self.feature_finder.setUpright(upright)
    elif feature_extractor == 'SIFT':
      self.feature_finder = cv2.xfeatures2d.SIFT_create(edgeThreshold=20,sigma=1.1)
    else:
      raise 'Feature extractor no encontrado'

  def compare(self,img1,img2):
    self.features_img1 = self.find_features(img1) 
    self.features_img2 = self.find_features(img2)

    return self.flann.knnMatch(self.features_img1[1],self.features_img2[1],k=2)

  def compare_base64(self,image1_base64,image2_base64):
    img1 = self.base64_to_img(image1_base64)
    img2 = self.base64_to_img(image2_base64)

    return self.compare(img1,img2)

  def are_similar(self,img1,img2):
    self.matches = self.compare(img1,img2)
    self.good_matches = []

    for m,n in self.matches:
      if m.distance < self.__PORC_DISTANCE*n.distance:
        self.good_matches.append(m)

    return (self.good_matches > self.MIN_MATCH_COUNT)

  def find_features(self,img):
    return self.feature_finder.detectAndCompute(img,None)

  def bytes_to_img(self,image_bytes):
    nparr = np.fromstring(image_bytes, np.uint8)
    return cv2.imdecode(nparr, 0)

  def base64_to_img(self,image_base64):
    return self.bytes_to_img(base64.b64decode(image_base64))

  def compare_and_draw_base64(self,img1,img2):
    self.compare_and_draw(self.base64_to_img(img1),self.base64_to_img(img2))

  def compare_and_draw(self,img1,img2):
    if self.are_similar(img1,img2):
      src_pts = np.float32([ self.features_img1[0][m.queryIdx].pt for m in good ]).reshape(-1,1,2)
      dst_pts = np.float32([ self.features_img2[0][m.trainIdx].pt for m in good ]).reshape(-1,1,2)

      M, mask = cv2.findHomography(src_pts,dst_pts,cv2.RANSAC,5.0)
      matchesMask = mask.ravel().tolist()

      h,w = img1.shape
      pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
      dst = cv2.perspectiveTransform(pts,M)

      img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3,cv2.LINE_AA)
    else:
      print "Not enough matches are found - %d/%d" % (len(self.good_matches),self.MIN_MATCH_COUNT)
      matchesMask = None

    draw_params = dict(matchColor = (0,255,0),
                       singlePointColor = (255,0,0),
                       matchesMask = matchesMask,
                       flags = 0)

    img3 = cv2.drawMatchesKnn(img1,self.features_img1[0],img2,self.features_img2[0],self.good_matches,None,**draw_params)

    plt.imshow(img3,),plt.show()