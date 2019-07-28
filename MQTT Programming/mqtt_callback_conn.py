import paho.mqtt.client as mqtt
import time
import sys

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True
        print("connected OK")
    else:
        print('Bad connection Returen code= ', rc)
        client.bad_connected_flag = True

mqtt.Client.connected_flag = False
mqtt.Client.bad_connected_flag = False
broker = 'iot.eclipse.org'
client = mqtt.Client()
client.on_connect = on_connect
print('Connecting to broker ', broker)

try:
    client.connect(broker)
except:
    print("can't connect")
    sys.exit(1)
          
client.loop_start()
while not client.connected_flag and not client.bad_connected_flag:
    print('In wait loop')
    time.sleep(1)

    if client.bad_connected_flag == True:
        client.loop_stop()
        sys.exit(1)
    
print('in Main Loop')
client.publish('house/main-light', 'off')
time.sleep(4)
client.loop_stop()
client.disconnect()
