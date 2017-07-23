#!/bin/python3

import paho.mqtt.client as mqtt
import uuid
import logging

class MqttWrapper:

  def __init__(self,host):
    self.client = mqtt.Client(uuid.uuid1().hex,clean_session=False)
    self.client.connect(host)
    self.client.loop_start()

  def send(self,topic,message):
    self.client.subscribe(topic)
    result = self.client.publish(topic,message,qos=1,retain=False)
    logging.debug('Se publico y obtuvo los siguientes resultados: '+ str(result[0] == MQTT_ERR_SUCCESS ))

  def close(self):
    self.client.loop_stop()
    self.client.disconnect()


