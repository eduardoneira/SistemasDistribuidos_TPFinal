#!/bin/python3

import unittest
import sys

sys.path.insert(0, '../')
from modules.LBPH_wrapper import *

class TestLBPHWrapper(unittest.TestCase):

  def setUp(self):
    self.lbph = LBPHWrapper(50,100)

  def test_against_database(self):
    train = []
    labels = []
    predict = []
    
    for i in range(1,40):
      for j in range(1,10):
        with open('./att_faces/orl_faces/s'+str(i)+'/'+str(j)+'.pgm','rb') as f:
          if (j < 8): 
            train.append(self.lbph.bytes_to_img(f.read()))
            labels.append(i)
          else:
            predict.append(self.lbph.bytes_to_img(f.read()))

    self.lbph.train(train,labels)
    
    for img in predict:
      self.lbph.predict(img)

if __name__ == '__main__':
  unittest.main()
