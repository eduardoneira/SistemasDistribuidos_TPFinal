#!/bin/python3

import json
from modules.LBPH_wrapper import *
from modules.pika_wrapper_receive import *
from modules.pika_wrapper_publish import *
from modules.logger import *
from modules.graceful_killer import *



def handle_message(ch, method, properties, body):
  #do shit
  client.send("message","routing key")

if __name__ == '__main__':

  with open('config.json') as config_file:
    config = json.load(config_file)

  set_logger(config['logging_level'],config['logging_level'])

  face_recognizer = LBPHWrapper(config['MIN_MATCH_PROBABILITY'],
                                config['MIN_UPDATE_PROBABILITY'])

  #Should always be localhost for server and client
  client = PikaWrapperPublisher('localhost',config['exchange_response'])
  
  server = PikaWrapperReceiver('localhost',config['queue_request'])
  server.set_receive_callback(handle_message)

  server.start_consuming()
