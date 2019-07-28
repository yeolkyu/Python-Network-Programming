#! /usr/bin/env python
"""
Python implementation of an 'echo' tcp server: echo all data it receives.
This is the simplest possible server, servicing a single request only.
"""

from socket import *

ECHO_PORT = 2500
BUFSIZE = 1024

s = socket(AF_INET, SOCK_STREAM)
s.bind(('', ECHO_PORT))
s.listen(1) #최대 대기 틀라이언트 수
print("Waiting for clients...")

conn, (remotehost, remoteport) = s.accept()
print('connected by', remotehost, remoteport)
while True:
    data = conn.recv(BUFSIZE)
    if not data:
        break
    print("Received message: ", data.decode())
    conn.send(data)
conn.close()
