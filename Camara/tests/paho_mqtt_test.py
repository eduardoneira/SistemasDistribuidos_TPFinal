#!/bin/python3

# import unittest
# import sys
import paho.mqtt.client as mqtt
# sys.path.insert(0, '../')
# from modules.mock_camera import *

# class TestClientMQTT(unittest.TestCase):

#   def setUp(self):
    
#   def test_send_message(self):

#   def tearDown(self):

if __name__ == '__main__':
  # unittest.main()

  broker_address="localhost" 
  client = mqtt.Client("test1") #create new instance
  client.connect(broker_address) #connect to broker
  client.publish("pahodemo/test","Hello World!",qos=1)
  client.disconnect()