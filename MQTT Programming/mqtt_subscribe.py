#mqtt_subscribe.py
import paho.mqtt.subscribe as subscribe

def message(client, userdata, message):
    print("%s : %s" % (message.topic, message.payload.decode()))

subscribe.callback(message, "test/dy", hostname="test.mosquitto.org")
print("Waiting...")
while True:
    pass
