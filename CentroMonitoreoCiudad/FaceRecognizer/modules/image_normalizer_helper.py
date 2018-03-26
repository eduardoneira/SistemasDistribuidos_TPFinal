#/bin/python3

import cv2

def resize_image(image, dimensions):
    return cv2.resize(image, dimensions, cv2.INTER_CUBIC)

def black_and_white(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   
def histogram_equalization(image):
    return cv2.equalizeHist(image)

def histogram_equalization2(image):
    return cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)).apply(image)