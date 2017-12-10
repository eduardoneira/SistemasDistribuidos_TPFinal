#!/usr/bin/python3

from worker import *
import unittest
import glob
import pdb

class RequestTest(unittest.TestCase):
  
  def setUp(self):
    with open('./config.json') as config_file:
      self.config = json.load(config_file)

    self.config['db']['dbname'] = 'test'

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

  def __create_request_check_existance(self, images):
    request = {}
    request['type'] = str(self.config['requests']['existance'])
    request['images'] = {}

    for i, image in enumerate(images):
      with open(image, 'rb') as file:
        request['images'][i] = base64.b64encode(file.read()).decode('utf-8')

    return json.dumps(request)

  def __create_request_trajectory(self, dni):
    request = {}
    request['type'] = str(self.config['requests']['trajectory'])
    request['dni'] = dni

    return json.dumps(request)

  def test_upload_query(self):
    request = self.__create_request_upload('38155623', 'missing', 'edu', 'neira', glob.glob("tests/*.jpg"))
    handler = QueryHandler(self.config)
    response = json.loads(handler.handle(request.encode()))
    
    self.assertEqual(response['status'], 'OK')

  def test_trajectory(self):
    request = self.__create_request_upload('38155623', 'missing', 'edu', 'neira', glob.glob("tests/*.jpg"))
    handler = QueryHandler(self.config)
    handler.handle(request.encode())

    request = self.__create_request_trajectory('38155623')
    response = json.loads(handler.handle(request.encode()))
    
    self.assertEqual(response['status'], 'NOT OK')

  def test_check_existance(self):
    request = self.__create_request_check_existance(glob.glob("tests/*.jpg"))
    handler = QueryHandler(self.config)
    response = json.loads(handler.handle(request.encode()))
    
    self.assertEqual(response['status'], 'NOT OK')

  def tearDown(self):
    connection_str = "dbname={} user={} host={} password={}".format(self.config['db']['dbname'], 
                                                                    self.config['db']['user'], 
                                                                    self.config['db']['host'], 
                                                                    self.config['db']['password'])
    
    connection_db = psycopg2.connect(connection_str)
    connection_db.autocommit = True
    cursor = connection_db.cursor()
    cursor.execute("Truncate PersonImage CASCADE")
    cursor.execute("Truncate Person CASCADE")
    cursor.close()
    connection_db.close()

if __name__ == '__main__':
  unittest.main()
