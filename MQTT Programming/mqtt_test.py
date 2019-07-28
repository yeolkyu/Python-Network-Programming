import paho.mqtt.client as mqtt
import time
cnt = 1

def On_Connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("RPi/LED")

# The callback for when a PUBLISH message is received from the server.
def On_Message(client, userdata, msg):
    cmd = msg.payload.decode()
    print(msg.topic+" "+cmd)

client = mqtt.Client()
client.on_connect = On_Connect
client.on_message = On_Message

client.connect("iot.eclipse.org", 1883, 60)
client.loop_start()

while True:
    client.publish("mqtt/SWITCH", "Hello"+str(cnt))
    cnt += 1
    time.sleep(2)
