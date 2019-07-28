import json
import socket as sock
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
#Data is connected to GPIO3(pin=5)
GPIOpin = 3

hum, temp = Adafruit_DHT.read_retry(sensor, GPIOpin)
data = '{"room":{"temperature": %0.1f, "humidity": %0.1f}}'%(temp, hum) #전송 데이터

c_sock = sock.socket()
c_sock.connect(('127.0.0.1', 2500))
j_sensor = json.dumps(data) #JSON 포멧으로 변환
c_sock.send(j_sensor.encode()) #JSON 포멧을 인코딩하여 전송
c_sock.close()
