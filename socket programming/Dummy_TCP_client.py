# Dummy_TCP_client.py
import socket
import sys
import pickle

comSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

svrIP = input(("Server IP(default: 127.0.0.1): "))
if svrIP == '':
    svrIP = '127.0.0.1'
port = input('port(default: 2500): ')
if port == '':
    port = 2500
else:
    port = int(port)
comSocket.connect((svrIP, port))
print('Connected to '+svrIP)

while True:
   sendData = input("Message to send: ")
   if not sendData:
      sendData = ' '
   try:
       nBytes = comSocket.send(sendData.encode())
   except:
       print("송신 연결이 종료되었습니다")
       retry = input("계속?(y/n) ")
       if retry == 'n':
           comSocket.close()
           break
       else:
           continue
   #else:
   #    print("{} bytes sent".format(nBytes))
       
   try:
       print('Received message: {0}'.format(comSocket.recv(1024).decode()))
   except:
       print("수신 연결이 종료되었습니다")
       comSocket.close()
       break