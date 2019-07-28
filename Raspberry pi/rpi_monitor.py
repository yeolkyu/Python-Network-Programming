import socket
import RPi.GPIO as GP

GP.setmode(GP.BCM)
GP.setwarnings(False)
GP.setup(23, GP.IN)

sock = socket.socket()
addr = ('', 2500)
sock.bind(addr)
sock.listen(1)
print("Waiting for connection")
c_sock, c_addr = sock.accept()
while 1:
    data = c_sock.recv(1024)
    if data.decode().upper() == "SW1":
        state = GP.input(23)
        print("State of switch 1 is {}".format(state))
        if state == 1:
            msg = "Switch 1 is ON"
        else:
            msg = "Switch 1 is OFF"
        c_sock.send(msg.encode())
    else:
        c_sock.send("Invalid command. Try again")
