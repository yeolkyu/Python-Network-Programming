import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

LED = 18
SWITCH = 23

def Rpi_Set():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED, GPIO.OUT)
    GPIO.setup(SWITCH, GPIO.IN)
    GPIO.output(LED, GPIO.LOW) # LED OFF initially

def On_Connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("RPi/LED")

# The callback for when a PUBLISH message is received from the server.
def On_Message(client, userdata, msg):
    cmd = msg.payload.decode()
    print(msg.topic+" "+cmd)
    if cmd == "ON": # turn on LED
        GPIO.output(LED, GPIO.HIGH)
    elif cmd == "OFF": #turn off LED
        GPIO.output(LED, GPIO.LOW)
    else:
        print("Invalid message")

client = mqtt.Client()
client.on_connect = On_Connect
client.on_message = On_Message

client.connect("iot.eclipse.org", 1883, 60)
client.loop_start()

while True:
	state = GPIO.input(SWITCH)
	if state == 1:
		s_msg = "SWITCH ON"
	else:
		s_msg = "SWITCH OFF"
    client.publish("RPi/SWITCH", s_msg)
    time.sleep(2)