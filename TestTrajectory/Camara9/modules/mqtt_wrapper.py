#!/bin/python3

import paho.mqtt.client as mqtt
import uuid
import logging

class MqttWrapper:

  def __init__(self,host):
    self.client = mqtt.Client(client_id=uuid.uuid1().hex,
                              clean_session=True)
    self.client.connect(host)
    self.client.loop_start()

  def send(self,topic,message):
    result = self.client.publish( topic=topic,
                                  payload=message,
                                  qos=1)

    logging.debug('Se publico en '+topic+' con return value: '+str(result[0]))

  def close(self):
    self.client.loop_stop()
    self.client.disconnect()


