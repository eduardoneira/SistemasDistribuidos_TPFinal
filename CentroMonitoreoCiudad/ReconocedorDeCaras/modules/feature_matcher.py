#!/bin/python3

import numpy as np
import cv2
from tkinter import *
from matplotlib import pyplot as plt 

class FeatureMatcher:

  def __init__(self,min_match_count):
    self.MIN_MATCH_COUNT = min_match_count
    self.sift = cv2.xfeatures2d.SIFT_create()

    #Setting FLANN matcher
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    self.flann = cv2.FlannBasedMatcher(index_params, search_params)

  def compare(self,img1,img2):
    sift_hash1 = self.sift_hash(img1)
    sift_hash2 = self.sift_hash(img2)
    matches = self.flann.knnMatch(sift_hash1[1],sift_hash2[1],k=2)

    good = []
    for m,n in matches:
      if m.distance < 0.7*n.distance:
          good.append(m)

    return good

  def compare_base64(self,image1_base64,image2_base64):
    img1 = self.base64_to_img(image1_base64)
    img2 = self.base64_to_img(image2_base64)

    return self.compare(img1,img2)

  def are_similar(self,img1,img2):
    matches = self.compare(img1,img2)
    return (len(matches) > self.MIN_MATCH_COUNT)

  def sift_hash(self,img):
    keypoints, descriptor = self.sift.detectAndCompute(img,None)
    return (keypoints,descriptor)

  def bytes_to_img(self,image_bytes):
    nparr = np.fromstring(image_bytes, np.uint8)
    img_np = cv2.imdecode(nparr, 0)
    return img_np

  def base64_to_img(self,image_base64):
    return self.bytes_to_img(base64.b64decode(image_base64))

  def compare_and_draw(self,img1,img2):
    sift_hash1 = self.sift_hash(img1)
    sift_hash2 = self.sift_hash(img2)
    matches = self.flann.knnMatch(sift_hash1[1],sift_hash2[1],k=2)

    good = []
    for m,n in matches:
      if m.distance < 0.7*n.distance:
          good.append(m)

    if len(good)>self.MIN_MATCH_COUNT:
      src_pts = np.float32([ sift_hash1[0][m.queryIdx].pt for m in good ]).reshape(-1,1,2)
      dst_pts = np.float32([ sift_hash2[0][m.trainIdx].pt for m in good ]).reshape(-1,1,2)
      M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
      matchesMask = mask.ravel().tolist()
      h,w = img1.shape
      pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
      dst = cv2.perspectiveTransform(pts,M)
      img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)
    else:
      print( "Not enough matches are found - {}/{}".format(len(good), self.MIN_MATCH_COUNT) )
      matchesMask = None

    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                       singlePointColor = None,
                       matchesMask = matchesMask, # draw only inliers
                       flags = 2)
    img3 = cv2.drawMatches(img1,sift_hash1[0],img2,sift_hash2[0],good,None,**draw_params)
    plt.imshow(img3, 'gray'),plt.show()
