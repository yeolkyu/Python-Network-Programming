#mqtt_single_pub.py
import paho.mqtt.publish as publish
import time
import socket

print("Sending 0...")
publish.single("/test", "1st message", hostname = "iot.eclipse.org")
time.sleep(1)
print("Sending 1...")
publish.single("/test", "2nd message", hostname = "iot.eclipse.org")
