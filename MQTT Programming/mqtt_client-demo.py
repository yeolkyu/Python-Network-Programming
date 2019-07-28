# MQTT Client demo
# Continuously monitor two different MQTT topics for data
# check if the received data matches two predefined 'commands'

import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
        print("Connectd with result code "+str(rc))

        # Subscribing in on_connect()
        # reconnect then subscription will be renewed
        client.subscribe("CoreElectronics/test")
        client.subscribe("CoreElectronics/topic")

# The callback for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

        if msg.payload.decode() == "Hello":
            print("Receiving message: #1, do something")
            # Do something

        if msg.payload.decode() == "World!":
            print("Receiving message #2, do something else")
            # Do something else

# Create an MQTT client and attach out routine to it.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("iot.eclipse.org", 1883, 60)

client.loop_forever()
