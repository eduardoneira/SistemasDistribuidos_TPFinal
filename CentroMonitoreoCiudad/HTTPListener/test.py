#!/usr/bin/python3

from worker import *
import unittest
import glob
import pdb

class RequestTest(unittest.TestCase):
  
  def setUp(self):
    #TODO: remove files and truncate db
    with open('./config.json') as config_file:
      self.config = json.load(config_file)

  def __create_request_upload(self, dni, state, name, surname, images):
    request = {}
    request['type'] = str(self.config['requests']['upload'])
    request['dni'] = dni
    request['state'] = str(self.config['requests'][state])
    request['name'] = name
    request['surname'] = surname
    request['images'] = {}
    for i, image in enumerate(images):
      with open(image, 'rb') as file:
        request['images'][i] = base64.b64encode(file.read()).decode('utf-8')

    return json.dumps(request)

  def test_upload_query(self):
    request = self.__create_request_upload('38155623', 'missing', 'edu', 'neira', glob.glob("tests/*.jpg"))
    handler = QueryHandler(self.config)
    response = json.loads(handler.handle(request.encode()))
    
    self.assertEqual(response['status'], 'OK')

  def test_check_existance(self):
    

if __name__ == '__main__':
  unittest.main()
