#mqtt_subscribe_simple.py
import paho.mqtt.subscribe as subscribe
import RPi.GPIO as GP
import time

GP.setmode(GP.BCM)
GP.setwarnings(False)
GP.setup(18, GP.OUT)
GP.setup(23, GP.IN)

#topics = ['RPi/SWITCH-1']
topic = 'lamp'
print('Topic: ', topic)
while True:
    m = subscribe.simple(topic, hostname="iot.eclipse.org", retained=False, msg_count=1)
    r_msg = m.payload.decode()
    print('Message: ', r_msg)
    if r_msg == "on":
        GP.output(18, 1)
    else:
        GP.output(18, 0)
