#mqtt callback_conn2.py
import paho.mqtt.client as mqtt
import time
import sys

def on_log(client, userdata, level, buf):
    print("log: ", buf)

def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected flags"+" result code "+str(rc))
    client.connected_flag = False
    
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True
        print("connected OK")
    else:
        print('Bad connection Returen code= ', rc)

mqtt.Client.connected_flag = False
broker = 'test.mosquitto.org'
client = mqtt.Client()
client.on_log = on_log
client.on_connect = on_connect
client.on_disconnet = on_disconnect
print('Connecting to broker ', broker)

client.loop_start()

try:
    client.connect(broker)
    while not client.connected_flag:
        print('In wait loop')
        time.sleep(1)
except:
    print("connection failed")
    sys.exit(1)
          
run_flag = True
count=1
while run_flag:
    print('in Main Loop')
    msg = "test message" + str(count)
    ret = client.publish("test/dy", msg, 0)
    print("publish", ret)
    count += 1
    time.sleep(4)
                         
client.loop_stop()
client.disconnect()
