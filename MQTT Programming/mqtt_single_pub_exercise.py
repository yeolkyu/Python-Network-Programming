#mqtt_single_pub.py
import paho.mqtt.publish as publish
import socket

ip_addr = socket.gethostbyname(socket.gethostname())
publish.single("/test", ip_addr, hostname = "iot.eclipse.org")

while True:
	msg = input("Type in message: ")
	if msg.lower() == "q":
		break
	publish.single("/test", msg, hostname = "iot.eclipse.org")