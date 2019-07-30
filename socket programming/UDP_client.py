#!/usr/bin/env python3 
# -*- coding: utf8 -*- 
import socket
BUFFSIZE = 1024
port = 2500

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
msg = "Hello UDP server"
sock.sendto(msg.encode(),('192.168.0.15', port))
data, addr = sock.recvfrom(BUFFSIZE)
print("Server says:", data.decode())
