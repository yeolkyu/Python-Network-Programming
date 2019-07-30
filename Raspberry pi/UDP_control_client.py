import socket
BUFFSIZE = 1024
port = 2500
host = input("Server IP Address: ")
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
while True:
    msg = input("Command(ON/OFF): ")
    msg = msg.upper()
    sock.sendto(msg.encode(),(host, port))
    print("LED가 {}되었는지 확인하시오", msg)
