#!/bin/python3

import numpy as np
import cv2
import base64
from tkinter import *
from matplotlib import pyplot as plt 

class FeatureMatcher:

  def __init__(self,min_match_count,threshold):
    self.MIN_MATCH_COUNT = min_match_count
    self.feature_finder = cv2.xfeatures2d.SURF_create(threshold)

    #Setting FLANN matcher
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 100)
    self.flann = cv2.FlannBasedMatcher(index_params, search_params)

  def compare(self,img1,img2):
    features_img1 = self.find_features(img1) 
    features_img2 = self.find_features(img2)
    matches = self.flann.knnMatch(features_img1[1],features_img2[1],k=2)

    return matches

  def compare_base64(self,image1_base64,image2_base64):
    img1 = self.base64_to_img(image1_base64)
    img2 = self.base64_to_img(image2_base64)

    return self.compare(img1,img2)

  def are_similar(self,img1,img2):
    matches = self.compare(img1,img2)
    
    good_matches = 0

    for m,n in matches:
      if m.distance < 0.7*n.distance:
        good_matches += 1

    return (good_matches > self.MIN_MATCH_COUNT)

  def find_features(self,img):
    keypoints, descriptor = self.feature_finder.detectAndCompute(img,None)
    return (keypoints,descriptor)

  def bytes_to_img(self,image_bytes):
    nparr = np.fromstring(image_bytes, np.uint8)
    img_np = cv2.imdecode(nparr, 0)
    return img_np

  def base64_to_img(self,image_base64):
    return self.bytes_to_img(base64.b64decode(image_base64))

  def compare_and_draw_base64(self,img1,img2):
    self.compare_and_draw(self.base64_to_img(img1),self.base64_to_img(img2))

  def compare_and_draw(self,img1,img2):
    kp1, des1 = self.find_features(img1) 
    kp2, des2 = self.find_features(img2)
    matches = self.flann.knnMatch(des1,des2,k=2)
    
    matchesMask = [[0,0] for i in range(len(matches))]

    for i,(m,n) in enumerate(matches):
      if m.distance < 0.7*n.distance:
        matchesMask[i]=[1,0]

    draw_params = dict(matchColor = (0,255,0),
                       singlePointColor = (255,0,0),
                       matchesMask = matchesMask,
                       flags = 0)

    img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)

    plt.imshow(img3,),plt.show()