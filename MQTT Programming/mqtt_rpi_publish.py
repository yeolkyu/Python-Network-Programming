# -*- coding: utf-8 -*-
# An example show the usage of publish.single helper function.

import paho.mqtt.publish as publish
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)
print("Checking SWITCH on GPIO23")
While True:
	led_state = GPIO.input(23)
	if led_state == 1:
		msg = "SWITCH ON"
	else:
		msg = "SWITCH OFF"
	publish.single("RPi/LED-1", msg, hostname="iot.eclipse.org")
	time.sleep(1) # 1초 대기