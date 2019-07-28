# MQTT Publish demo
# Publish two message, to two different topics

import paho.mqtt.publish as publish

publish.single("mqtt/test", "Hello", hostname="iot.eclipse.org")
publish.single("CoreElectronics/topic", "World!", hostname="iot.eclipse.org")
print("Done")