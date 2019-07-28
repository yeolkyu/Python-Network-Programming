# This shows an example of using the subscribe.simple helper function.

import paho.mqtt.subscribe as subscribe

topics = ['RPi/SWITCH-1']
print('Topic: ', topics[0])
while True:
	m = subscribe.simple(topics, hostname="iot.eclipse.org", retained=False, msg_count=1)
	print('Message: ', m.payload.decode())
#input('Type ENTER to finish')