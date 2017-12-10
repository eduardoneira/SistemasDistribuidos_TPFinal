#!/usr/bin/python3

from modules.query_handler import * 
from modules.rpc_server_rabbitmq import *
from modules.graceful_killer import *

def handle(body):
  return handler.handle(body)

if __name__ == '__main__':
  print('Configurando CMC Query Handler Worker')

  with open('./config.json') as config_file:
    config = json.load(config_file)

  set_logger(config['logger']['logging_level'])

  server = RPCServer(host=config['network']['broker_client_host'],
                     queue=config['network']['queue_client'],
                     request_callback_main=handle)

  handler = QueryHandler(config)

  graceful_killer = GracefulKiller()
  graceful_killer.add_connection(handler)
  graceful_killer.add_connection(server)

  print('Query Handler Worker configurando - Comenzando a escuchar mensajes de los clientes')
  server.start()
