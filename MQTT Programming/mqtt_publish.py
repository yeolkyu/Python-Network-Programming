#mqtt_publish.py
import paho.mqtt.publish as publish

#publish.single("mqtt/test", "Is there anyone?", hostname = "iot.eclipse.org")

while True:
	msg = input("Type in message: ")
	if msg.lower() == "q":
		break
	publish.single("mqtt/test", msg, hostname = "iot.eclipse.org")
