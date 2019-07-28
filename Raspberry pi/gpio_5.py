import RPi.GPIO as GPIO
import time

def mycallback(channel):
    global count, flag, SEG
    count += 1
    if count == 10:
        flag = 0
        GPIO.output(18, 1)
        return
    print('Button {} pressed'.format(count))
    LEDbit = bin(count).split('b')[1].zfill(4)
    for i in range(4):
        GPIO.output(SEG[i], int(LEDbit[i]))
        
SEG = [26,19,13,6] #A4, A3, A2, A1 for 7-segment
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(2, GPIO.IN)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, 0)

for i in SEG:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, 0) #turn off initially

count = 0
flag = 1
GPIO.add_event_detect(2, GPIO.RISING, callback=mycallback)


while flag == 1:
    continue

GPIO.remove_event_detect(2)
print('The END')
