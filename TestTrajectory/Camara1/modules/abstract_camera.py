#!/bin/python3

import shutil
import os
import base64
import logging

class AbstractCamera:

  CONST_PATH_IMG = './img/'
  CONST_INVALID = 'INVALID'

  def __init__(self):

    self.__id = 1

  def get_frame(self):
    raise Exception('Should override method get_frame')

  def PATH_IMG(self):
    return self.CONST_PATH_IMG

  def INVALID(self):
    return self.CONST_INVALID

  def base64(self,file):
    return base64.b64encode(file.read())
