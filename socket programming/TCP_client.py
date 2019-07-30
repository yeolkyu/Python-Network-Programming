# TCP_client.py
import socket
import sys

comSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

svrIP = input(("Server IP(127.0.0.1): "))
if svrIP == '':
	svrIP = '127.0.0.1'
port = input('port(2500): ')
if port == '':
	port = 2500
else:
	port = int(port)
comSocket.connect((svrIP, port))
print('Connected to '+svrIP)

while True:
   sendData = input("Sending message: ")
   if len(sendData) == 0:
      sendData = ' '
   comSocket.send(sendData.encode())
   print('Received message: {0}'.format(comSocket.recv(1024).decode()))