import socket
port = 2500
maxsize = 1024
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(('', port))
while True:
    data, addr = sock.recvfrom(maxsize)
    print("Received message: ", data.decode())
    print(addr)
    resp = "UDP server sending data... " + str(addr)
    sock.sendto(resp.encode(),addr)
