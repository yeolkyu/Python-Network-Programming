# gpio_1.py
import RPi.GPIO as GP
import time

#setup GPIO pin numbering
GP.setmode(GP.BCM)
GP.setwarnings(False)
GP.setup(18, GP.OUT) #setup GPIO18 as OUT. LED connected
GP.setup(23, GP.IN) #setup GPIO23 as IN. Switch connected
while True:
    SW = GP.input(23)
    if SW == 1:
        print("Switch is ON")
    else:
        print("Switch is OFF")
    GP.output(18, SW)
    time.sleep(2)

