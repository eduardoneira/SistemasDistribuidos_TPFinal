#!/bin/python3

import pika
import json

class FaceRecognizerClient(object):
  def __init__(self,host,queue_send,queue_receive):
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))

    self.channel = self.connection.channel()

    self.channel.queue_declare( queue=queue_receive,
                                exclusive=True)

    self.channel.basic_consume(self.on_response, 
                               no_ack=True,
                               queue=queue_receive)
    
    self.queue_send = queue_send
    self.queue_receive = queue_receive

  def on_response(self, ch, method, props, body):
    self.response = body

  def publish(self, message):
    self.response = None
    self.channel.basic_publish(exchange='',
                               routing_key=self.queue_send,
                               properties=pika.BasicProperties(
                                             reply_to = self.queue_receive
                                          ),
                               body=message)
    while self.response is None:
        self.connection.process_data_events()
    
    return self.response

  def update(self,image):
    message = { 
                'type': 'update',
                'image': image
              }

    response = json.loads(self.publish(json.dumps(message)))
    return response['id']

  def predict(self,images):
    message = { 
            'type': 'predict',
            'image': images
          }
              
    response = json.loads(self.publish(json.dumps(message)))
    return response['ids']

  def close(self):
    self.connection.close()