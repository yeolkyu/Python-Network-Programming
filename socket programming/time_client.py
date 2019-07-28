import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect(('localhost', 5000))
s.connect(('localhost', 5000))
print("현재 시각: ", s.recv(1024).decode())
