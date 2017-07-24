#!/bin/python3

import json
from modules.graceful_killer import *
from modules.logger import *
from modules.pika_wrapper_subscriber import *

def callback(ch, method, properties, body):
  #TODO: OPENCV AND RESEND
  logging.debug('Message received: %s', body)
  print(" [x] Received %r" % body)

if __name__ == '__main__':
  print('Configurando CMB')

  with open('config.json') as config_file:    
    config = json.load(config_file)

  set_logger(config['logging_level'])

  server = PikaWrapperSubscriber( host='localhost',
                                  topic=config['topic_camera'],
                                  queue=config['queue'])

  killer = GracefulKiller()
  killer.add_connection(server)

  server.set_receive_callback(callback)

  print(' [*] Esperando mensajes para procesar. Para salir usar CTRL+C')
  server.start_consuming()