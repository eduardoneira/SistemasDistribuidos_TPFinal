#!/bin/python3

import paho.mqtt.client as mqtt
import uuid

class MqttWrapper:

  def __init__(self,host):
    self.client = mqtt.client(uuid.uuid1().hex,clean_session=False)
    self.client.connect(host)
    self.client.loop_start()

  def send(self,topic,message):
    self.client.publish(topic,message,qos=1,retain=False)

  def close(self):
    self.client.disconnect()


