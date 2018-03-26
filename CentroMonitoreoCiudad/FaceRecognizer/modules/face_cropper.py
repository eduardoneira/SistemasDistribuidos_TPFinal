#!/bin/python3

import math
import cv2
import base64
import numpy as np
from modules.opencv_helper import *
from modules.image_normalizer_helper import *

class FaceCropper():

    PATH_HAAR = './haarcascade/haarcascade_frontalface_alt.xml'

    def __init__(self, config):
        self.face_cascade = cv2.CascadeClassifier(self.PATH_HAAR)
        self.scale_factor = config['scale_factor']
        self.min_neighbours = config['min_neighbours']
        self.min_size = (tuple(config['min_size']))
        self.default_size = (tuple(config['default_size']))
        self.shrink_factor = config['shrink_factor']

    def _crop(self, image):
        images = []

        image_eq = histogram_equalization(image)
        faces = self.face_cascade.detectMultiScale(image_eq,
                                                   self.scale_factor,
                                                   self.min_neighbours,
                                                   0,
                                                   self.min_size)
        
        for (x,y,w,h) in faces:
            cropped = resize_image(self.__center_target(image, y, h, x, w), self.default_size)
            images.append(image_to_bytes(cropped))

        return images

    def crop(self, image):
        return self._crop(bytes_to_image(image))

    def crop_base64(self, image):
        cv_image = bytes_to_image(base64.b64decode(image))
        return list(map(lambda img: base64.b64encode(img).decode('utf-8'), self._crop(cv_image)))

    def __center_target(self, image, y, h, x, w):
        deltaX = math.floor(w *(self.shrink_factor))
        deltaY = math.floor(h *(self.shrink_factor) / 3.0)
        return image[y+deltaY:y+h-deltaY, x+deltaX:x+w-deltaX]
