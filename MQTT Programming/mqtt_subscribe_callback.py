import paho.mqtt.subscribe as subscribe

def on_message(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))

subscribe.callback(on_message, "mqtt/test", hostname="iot.eclipse.org")
