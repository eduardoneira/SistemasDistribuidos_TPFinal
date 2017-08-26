#/bin/python3

import cv2

class ImageNormalizer:

  @staticmethod
  def resize(image,width,height):
    return cv2.resize(image,(width,height),cv2.INTER_CUBIC)

  @staticmethod
  def black_and_white(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
     
  @staticmethod
  def histogram_equalization(image):
    return cv2.equalizeHist(image)

  @staticmethod
  def normalize(image,width,height):
    new_image = resize(image,width,height)
    new_image = black_and_white(new_image)
    new_image = histogram_equalization(new_image)
    return new_image