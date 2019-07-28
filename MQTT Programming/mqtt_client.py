import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def On_Connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("mqtt/test")

# The callback for when a PUBLISH message is received from the server.
def On_Message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
#    client.publish("mqtt/resp", "resp" + msg.payload.decode())

client = mqtt.Client()
client.on_connect = On_Connect
client.on_message = On_Message

client.connect("iot.eclipse.org", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
