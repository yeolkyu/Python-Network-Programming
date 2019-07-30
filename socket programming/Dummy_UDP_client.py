import socket

c_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
svrIP = input(("Server IP(127.0.0.1): "))
if svrIP == '':
	svrIP = '127.0.0.1'
port = input('port(2500): ')
if port == '':
	port = 2500
else:
	port = int(port)
server = (svrIP, port)

message = input('-> ')
while message != 'q':
	c_sock.sendto(message.encode(), server)
	data, addr = c_sock.recvfrom(1024)
	print('<- ', data.decode())
	message = input('-> ')
c_sock.close()
