#!/bin/python3

import shutil
import os
import base64

class AbstractCamera:

  CONST_PATH_IMG = './img/'
  CONST_INVALID = 'INVALID'
  
  def __init__(self):
    shutil.rmtree(path = PATH_IMG(),
                  ignore_errors = True)
    os.mkdir(PATH_IMG())

    self.__id = 1

  def get_frame(self):
    raise Exception('Should override method get_frame')

  def PATH_IMG():
    return CONST_PATH_IMG

  def INVALID():
    return CONST_INVALID

  def base64(file):
    return base64.b64encode(file)
