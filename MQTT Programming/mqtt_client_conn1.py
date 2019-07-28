import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
        client.publish('test/dy', 'Test Message')
        time.sleep(4)
    else:
        print('Bad connection Returen code= ', rc)

broker = 'test.mosquitto.org'
client = mqtt.Client()
client.on_connect = on_connect
print('Connecting to broker ', broker)
client.loop_start()
client.connect(broker)

client.loop_stop()
