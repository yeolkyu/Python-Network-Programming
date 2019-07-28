import paho.mqtt.publish as publish

msgs = [{'topic':"mqtt/multiple", 'payload':"Hello"},
    ("mqtt/multiple", "World", 0, False)]
publish.multiple(msgs, hostname="test.mosquitto.org")