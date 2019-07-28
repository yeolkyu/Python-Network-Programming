#This program should be run on Raspberry Pi

import serial
port = "/dev/ttyACM0"
sp = serial.Serial(port, baudrate=9600, timeout=0)
sp.flushInput()
 
while True:
     if(sp.inWaiting()>0): #데이터 수신?
         in_msg = sp.read(1)
         print(ord(in_msg))
               