# -*- coding: utf-8 -*-
# An example show the usage of publish.single helper function.

import paho.mqtt.publish as publish
publish.single("mqtt/test", "Another Data", hostname="iot.eclipse.org")
