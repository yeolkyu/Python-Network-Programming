#!/usr/bin/env python3 
# -*- coding: utf8 -*- 
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.setblocking(True)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
addr = ("192.168.137.1", 2500)
sock.bind(addr)
sock.listen(1)

print("Waiting for connection...")
client, Raddr = sock.accept()
print("Client connected")

while True:
    try:
        r_msg = client.recv(2014)
    except Exception as e:
        print("연결이 종료되었습니다") #연결 강제 종료
        client.close()
        break
    else:
        print(r_msg.decode())
        
    try:
        client.send(r_msg)
    except:
        print("연결이 종료되었습니다")
        client.close()
        break
