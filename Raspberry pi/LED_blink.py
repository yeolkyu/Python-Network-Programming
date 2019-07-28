#!/usr/bin/env python3
# -*- coding: utf8 -*- 
#LED blinking
import RPi.GPIO as GP
GP.setmode(GP.BOARD)
GP.setup(12, GP.OUT)
p=GP.PWM(12, 0.5)
p.start(1)
input("Press Enter key to stop")
p.stop()
GP.cleanup()
