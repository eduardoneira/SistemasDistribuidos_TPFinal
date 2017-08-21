#/bin/python3

import cv2

class ImageNormalizer:

  def __init__(self,width,height):
    self.width = width
    self.height = height

  def __resize(image):
    print('resize')

  def __black_and_white(image):
    print('to black and white')

  def __distort(image):
    print('distort')

  def normalize(self,image):
    __black_and_white(image)
    __resize(image)
    __distort(image)

    return image