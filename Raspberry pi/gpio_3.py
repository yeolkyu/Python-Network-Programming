import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(2, GPIO.IN)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, 0)

GPIO.add_event_detect(2, GPIO.RISING)
count = 0

while True:
    if GPIO.event_detected(2):
        count += 1
        print("Button {} pressed ".format(count))
        if count == 10:
            GPIO.output(18, 1)
            break
GPIO.remove_event_detect(2)
