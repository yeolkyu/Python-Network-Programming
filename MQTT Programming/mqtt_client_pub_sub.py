import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
        print("Connection returned result: %d"%rc)
        client.subscribe(topic)

def on_message(client, userdata, msg):
    print("Received message: " + msg.payload.decode() + " on topic "  + msg.topic + " with QoS " + str(msg.qos))

SendMsg = "Hello World from loop program"

client = mqtt.Client()
topic = "mqtt/test"
client.on_connect = on_connect
client.on_message = on_message
client.loop_start()
client.connect("iot.eclipse.org", 1883, 60)
#client.connect("test.mosquitto.org", 1883, 60)

for i in range(4):
    time.sleep(3)
    client.publish(topic, f'{SendMsg} {i}')
time.sleep(3)