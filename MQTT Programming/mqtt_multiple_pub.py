import paho.mqtt.publish as publish
msgs = [{"topic": "paho/test/multiple", "/deneb": "multiple 1"}]
publish.multiple(msgs, hostname="localhost")
