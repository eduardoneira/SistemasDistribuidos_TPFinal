#!/bin/python3

import unittest
import sys

sys.path.insert(0, '../')
from modules.mock_camera import *

class TestCamera(unittest.TestCase):

  def setUp(self):
    self.camera = MockCamera()

  def test_create_camera(self):
    self.assertTrue(os.path.exists(self.camera.PATH_IMG_PROCESSED()))
    self.assertTrue(os.path.exists(self.camera.PATH_IMG()))

  def test_get_frame_invalid(self):
    self.assertEqual(self.camera.get_frame(),self.camera.INVALID())

  def test_get_frame_succesful(self):
    src_file = 'image_test_camera.jpg'
    dst_file = self.camera.PATH_IMG()+src_file
    shutil.copy(src_file,dst_file)

    img = self.camera.get_frame()
    self.assertNotEqual(img,self.camera.INVALID())
    self.assertTrue(len(img) > 0)

  def tearDown(self):
    shutil.rmtree(path = self.camera.PATH_IMG(),
                  ignore_errors = True)

    shutil.rmtree(path = self.camera.PATH_IMG_PROCESSED(),
                  ignore_errors = True)

if __name__ == '__main__':
  unittest.main()
