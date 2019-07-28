#mqtt_client_publish.py
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("iot.eclipse.org", 1883, 60)
rc, mid = client.publish("mqtt/test", "Hello Everyone") #rc=return code
print(str(rc))
