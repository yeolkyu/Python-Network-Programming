import socket
import RPi.GPIO as GP
GP.setmode(GP.BCM)
GP.setwarnings(False)
GP.setup(18, GP.OUT)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 2500))
print("Waiting for command")
while True:
    data, addr = sock.recvfrom(1024)
    if data.decode().upper() == "ON":
        GP.output(18, 1) #turn on LED
        sock.sendto("LED is ON".encode(), addr)
    elif data.decode().upper() == "OFF":
        GP.output(18, 0) #turn off lED
        sock.sendto("LED is OFF".encode(), addr)
    else:
        sock.sendto("Try again!!!".encode(), addr)