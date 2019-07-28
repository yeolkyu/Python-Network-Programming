#mqtt_client_sub.py
import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def On_Connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)
    
# The callback for when a PUBLISH message is received from the server.
def On_Message(client, userdata, msg):
    print(msg.topic+" "+msg.payload.decode())

topic = "mqtt/test"
client = mqtt.Client()
client.on_connect = On_Connect
client.on_message = On_Message

client.connect("iot.eclipse.org", 1883, 60)
#client.subscribe(topic)
client.loop_forever()
