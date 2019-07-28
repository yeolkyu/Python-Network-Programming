# This shows an example of using the subscribe.simple helper function.
#mqtt_subscribe_simple.py
import paho.mqtt.subscribe as subscribe

#topics = ['RPi/SWITCH-1']
topics = 'mqtt/test'
print('Topic: ', topics)
while True:
    m = subscribe.simple(topics, hostname="test.mosquitto.org", retained=False, msg_count=1)
    print('Received Message: ', m.payload.decode())
#input('Type ENTER to finish')
