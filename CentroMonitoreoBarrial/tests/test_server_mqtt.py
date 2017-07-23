import paho.mqtt.client as mqtt

broker_address="0.0.0.0" 
#broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("test1",clean_session=False) #create new instance
print("connecting to broker")
client.connect(broker_address) #connect to broker
print("Subscribing to topic","house/bulbs/bulb1")
client.subscribe("house/bulbs/bulb1")
print("Publishing message to topic","house/bulbs/bulb1")
client.publish("house/bulbs/bulb1","OFF",qos=1,retain=False)